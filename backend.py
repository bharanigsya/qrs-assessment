#!/usr/bin/env python3
"""
QRS Assessment Platform - Backend
Supports:
  - Postgres (Supabase / Neon) via DATABASE_URL  → permanent storage
  - Local JSON files as fallback (dev / no DB)

Local:  python backend.py  → http://localhost:5000
Render: set DATABASE_URL env var to your Supabase/Neon connection string
"""
import base64
import hashlib
import hmac
import html as _html
import json
import os
import re
import secrets
import threading
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory, abort
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE, "data", "assessments.json")
ADMIN_FILE = os.path.join(BASE, "data", "admin.json")
SETTINGS_FILE = os.path.join(BASE, "data", "settings.json")
BACKUP_DIR = os.path.join(BASE, "data", "backups")
MAX_BACKUPS = 30

def _clean_database_url(raw):
    """Normalize DATABASE_URL from Render/Supabase env (quotes, newlines, scheme)."""
    if not raw:
        return ""
    url = raw.strip().strip('"').strip("'").strip()
    # Remove accidental line breaks / spaces inside the URI
    url = "".join(url.split())
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    # Common paste error: double @@ before host
    if "@@" in url:
        url = url.replace("@@", "@", 1)
    # psycopg2 does not accept Supabase pooler flags like ?pgbouncer=true
    if "?" in url:
        base, query = url.split("?", 1)
        # Drop known-invalid / unnecessary query params for libpq/psycopg2
        drop = {"pgbouncer", "pgbouncer=true", "pgbouncer=1"}
        kept = []
        for part in query.split("&"):
            if not part:
                continue
            key = part.split("=", 1)[0].lower()
            if key == "pgbouncer":
                continue
            kept.append(part)
        url = base + ("?" + "&".join(kept) if kept else "")
    return url

DATABASE_URL = _clean_database_url(os.environ.get("DATABASE_URL", ""))
USE_DB = bool(DATABASE_URL) and DATABASE_URL.startswith("postgresql://")
if os.environ.get("DATABASE_URL") and not USE_DB:
    print("WARNING: DATABASE_URL is set but invalid. It must start with postgresql:// and be one line.")
_pg = None
_pg_pool = None

# SECURITY: static_folder=None. It used to be BASE, which served the ENTIRE project folder
# over HTTP (backend.py, data/admin.json with passwords, data/assessments.json, backups).
# Only the whitelisted front-end files below are served now.
app = Flask(__name__, static_folder=None)
app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024  # photos/videos are base64 in JSON
CORS(app, resources={r"/api/*": {"origins": "*"}})
STATIC_FILES = {"index.html", "admin.html", "test.html", "result.html",
                "questions.js", "styles.css", "qrs-logo.png"}
_file_lock = threading.RLock()


_pool_lock = threading.Lock()
_db_ready = False
_db_ready_lock = threading.Lock()


def _get_pool():
    global _pg_pool
    if _pg_pool is not None:
        return _pg_pool
    with _pool_lock:
        if _pg_pool is None:
            import psycopg2.pool
            if not DATABASE_URL or "://" not in DATABASE_URL:
                raise RuntimeError("DATABASE_URL missing or invalid")
            # Small pool: Render free tier + Supabase/Neon free tiers cap connections low.
            _pg_pool = psycopg2.pool.ThreadedConnectionPool(1, 8, DATABASE_URL, connect_timeout=20)
    return _pg_pool


def _acquire():
    """Get a live connection. Idle connections get dropped by Supabase/Render after sleep,
    so validate with SELECT 1 and transparently replace a dead one."""
    pool = _get_pool()
    last = None
    for _ in range(3):
        conn = pool.getconn()
        try:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return conn
        except Exception as e:  # dead connection
            last = e
            try:
                pool.putconn(conn, close=True)
            except Exception:
                pass
    raise last


@contextmanager
def pg(tx=False, _init=False):
    """Yield a pooled connection and ALWAYS give it back (the old code leaked a connection
    every time a query raised, which exhausted the 8-slot pool and froze the app).
    tx=True runs one transaction (commit on success, rollback on error)."""
    if not _init:
        ensure_db()
    conn = _acquire()
    broken = False
    try:
        if tx:
            conn.autocommit = False
        yield conn
        if tx:
            conn.commit()
    except Exception:
        try:
            if tx:
                conn.rollback()
        except Exception:
            broken = True
        raise
    finally:
        try:
            if not conn.closed:
                conn.autocommit = True
            else:
                broken = True
        except Exception:
            broken = True
        try:
            _get_pool().putconn(conn, close=broken)
        except Exception:
            pass


def _payload(v):
    return json.loads(v) if isinstance(v, str) else v


def ensure_db():
    """Create tables lazily so a cold/asleep DB at boot doesn't leave the app broken forever."""
    global _db_ready
    if _db_ready or not USE_DB:
        return
    with _db_ready_lock:
        if _db_ready:
            return
        db_init()
        _db_ready = True


def db_init():
    if not USE_DB:
        return
    with pg(_init=True) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                payload JSONB NOT NULL,
                status TEXT,
                name TEXT,
                email TEXT,
                updated_at TIMESTAMPTZ DEFAULT NOW(),
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS assessment_media (
                id SERIAL PRIMARY KEY,
                assessment_id TEXT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
                kind TEXT NOT NULL,
                data TEXT NOT NULL,
                meta JSONB DEFAULT '{}',
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE INDEX IF NOT EXISTS idx_media_assessment ON assessment_media(assessment_id);
            CREATE TABLE IF NOT EXISTS admin_users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'coordinator'
            );
            CREATE TABLE IF NOT EXISTS meta_backups (
                id SERIAL PRIMARY KEY,
                snapshot JSONB NOT NULL,
                note TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value JSONB NOT NULL,
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );
            """
        )
        # Seed admin users if empty (hashed; ON CONFLICT so two gunicorn workers booting
        # together can't crash each other)
        cur.execute("SELECT COUNT(*) FROM admin_users")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO admin_users (username, password, role) VALUES (%s,%s,%s), (%s,%s,%s) "
                "ON CONFLICT (username) DO NOTHING",
                ("admin", generate_password_hash("qrs@2026"), "admin",
                 "coordinator", generate_password_hash("qrs@coord"), "coordinator"),
            )
        # One-time migrate from local JSON if DB empty and file has data
        cur.execute("SELECT COUNT(*) FROM assessments")
        if cur.fetchone()[0] == 0 and os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    items = json.load(f)
                if isinstance(items, list) and items:
                    for a in items:
                        aid = a.get("id")
                        if not aid:
                            continue
                        cur.execute(
                            "INSERT INTO assessments (id, payload, status, name, email, updated_at) "
                            "VALUES (%s, %s::jsonb, %s, %s, %s, NOW()) ON CONFLICT (id) DO NOTHING",
                            (aid, json.dumps(a), a.get("status"), a.get("name"), a.get("email")),
                        )
                    print(f"Migrated {len(items)} assessments from JSON -> Postgres")
            except Exception as e:
                print("JSON->DB migrate skipped:", e)
        cur.close()
    print("Postgres storage ready")


# ---------- File fallback ----------
def ensure_data():
    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            json.dump(
                {
                    "users": [
                        {"user": "admin", "pass": generate_password_hash("qrs@2026"), "role": "admin"},
                        {"user": "coordinator", "pass": generate_password_hash("qrs@coord"), "role": "coordinator"},
                    ]
                },
                f,
                indent=2,
            )
    else:
        with open(ADMIN_FILE, "r") as f:
            try:
                cred = json.load(f)
            except Exception:
                cred = {}
        if "users" not in cred:
            cred = {
                "users": [
                    {"user": cred.get("user", "admin"), "pass": cred.get("pass", "qrs@2026"), "role": "admin"},
                    {"user": "coordinator", "pass": "qrs@coord", "role": "coordinator"},
                ]
            }
            with open(ADMIN_FILE, "w") as f:
                json.dump(cred, f, indent=2)


_last_backup_ts = 0.0


def backup_assessments_file(data):
    # Throttled: a photo arrives every ~10s per candidate and each save used to write a
    # full-size backup copy (base64 photos included), filling the disk within minutes.
    global _last_backup_ts
    if time.time() - _last_backup_ts < 120:
        return
    _last_backup_ts = time.time()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")
    path = os.path.join(BACKUP_DIR, f"assessments-{ts}.json")
    try:
        with open(path, "w") as f:
            json.dump(data, f)
        backups = sorted(
            (f for f in os.listdir(BACKUP_DIR) if f.startswith("assessments-")),
            reverse=True,
        )
        for old in backups[MAX_BACKUPS:]:
            try:
                os.remove(os.path.join(BACKUP_DIR, old))
            except OSError:
                pass
    except Exception as e:
        print("File backup failed:", e)


# ---------- Unified storage API ----------
def load_assessments():
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("SELECT payload FROM assessments ORDER BY created_at DESC")
            rows = cur.fetchall()
            cur.close()
        return [_payload(r[0]) for r in rows]
    with _file_lock:
        ensure_data()
        with open(DATA_FILE, "r") as f:
            return json.load(f)


def save_assessments(data):
    """FILE MODE ONLY: atomically replace the whole list. (The Postgres branch was removed:
    it re-upserted every row from a stale snapshot and deleted rows not in the list, which
    let one admin action overwrite candidates' live progress. DB mode now always touches
    exactly one row per operation.)"""
    with _file_lock:
        ensure_data()
        backup_assessments_file(data)
        tmp = DATA_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, DATA_FILE)


def get_one_assessment(aid):
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("SELECT payload FROM assessments WHERE id=%s", (aid,))
            row = cur.fetchone()
            cur.close()
        return _payload(row[0]) if row else None
    for a in load_assessments():
        if a.get("id") == aid:
            return a
    return None


def count_assessments():
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM assessments")
            n = cur.fetchone()[0]
            cur.close()
        return n
    return len(load_assessments())


def delete_one_assessment(aid):
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM assessments WHERE id=%s", (aid,))
            deleted = cur.rowcount > 0
            cur.close()
        return deleted
    with _file_lock:
        data = load_assessments()
        new_data = [a for a in data if a.get("id") != aid]
        if len(new_data) == len(data):
            return False
        save_assessments(new_data)
        return True


def insert_assessment(item):
    """Insert ONE new record. Returns False if the id already exists (no overwrite)."""
    aid = item["id"]
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO assessments (id, payload, status, name, email) VALUES (%s,%s::jsonb,%s,%s,%s) "
                "ON CONFLICT (id) DO NOTHING",
                (aid, json.dumps(item), item.get("status"), item.get("name"), item.get("email")),
            )
            ok = cur.rowcount > 0
            cur.close()
        return ok
    with _file_lock:
        data = load_assessments()
        if any(a.get("id") == aid for a in data):
            return False
        data.append(item)
        save_assessments(data)
        return True


def client_ip():
    """Best-effort client IP behind Render/proxy."""
    xff = (request.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
    if xff:
        return xff
    xri = (request.headers.get("X-Real-IP") or "").strip()
    if xri:
        return xri
    return (request.remote_addr or "").strip() or None


def attach_client_meta(body, existing=None):
    """Stamp IP / user-agent onto a CANDIDATE's record. (Previously also ran for admin saves,
    so an admin editing a record overwrote lastSeenIp - and could set clientIp - with the
    ADMIN's own IP. Callers now only use this for candidate requests.)"""
    if not isinstance(body, dict):
        return body
    existing = existing or {}
    ip = client_ip()
    ua = (request.headers.get("User-Agent") or "")[:300]
    if ip and not existing.get("clientIp"):
        body["clientIp"] = ip
    if ua and not existing.get("userAgent"):
        body["userAgent"] = ua
    if ip:
        body["lastSeenIp"] = ip
    return body


# Fields only an admin may change. A candidate's PUT is just JS in their browser, and their
# page re-sends its whole (possibly stale) local copy every few seconds, so without this a
# candidate could rewrite their own expiry/score/HR review, and stale copies silently
# overwrote HR's edits.
CANDIDATE_PROTECTED = {
    "id", "token", "name", "email", "mobile", "role", "level", "createdAt", "expiresAt", "scheduledAt", "linkValidFrom",
    "linkValidityHours", "duration", "extraMinutes", "allowMobile", "storePhotos", "totalMarks",
    "finalScore", "finalScoreBy", "finalScoreAt", "voiceScore", "codingScore", "codingEffort",
    "adminNote", "hrReplyToNote", "hrReplyShareOnCard", "hrReplyAt", "resultCardToken",
    "resultCardCreatedAt", "resultCardExpiresAt", "resultCardRevealed", "resultCardHours",
    "flagsCleared", "photoHistory", "videoHistory",
    "lastPhoto", "lastPhotoAt", "lastVideoAt",
}
# Hidden from the candidate's own GET (internal HR data + heavy media)
CANDIDATE_HIDDEN = {
    "adminNote", "finalScore", "finalScoreBy", "finalScoreAt", "voiceScore", "codingScore",
    "codingEffort", "hrReplyToNote", "hrReplyShareOnCard", "hrReplyAt", "resultCardToken",
    "resultCardCreatedAt", "resultCardExpiresAt", "resultCardRevealed", "resultCardHours",
    "flagsCleared", "clientIp", "userAgent", "lastSeenIp", "photoHistory", "videoHistory",
    "lastPhoto",
}
# Once a test is completed a candidate can no longer change these
FROZEN_AFTER_COMPLETE = ("score", "mcqScore", "mcqTotal", "mcqCorrect", "mcqCount",
                         "completedAt", "startedAt")


_ALLOWED_STATUS = {"pending", "in-progress", "completed", "flagged", "expired", "missed"}


def _esc(v, n):
    return _html.escape(str(v if v is not None else ""), quote=True)[:n]


def sanitize_candidate_body(body, existing):
    """Candidate-supplied text ends up in admin.html, which puts flag reasons, statuses and help
    messages into innerHTML. A candidate could therefore run script inside the ADMIN's session
    (stealing the admin token) by e.g. pasting `<img onerror=...>` (flag reasons include the
    pasted text!) or sending a crafted help-photo URL. Sanitise at the single write choke point."""
    if "status" in body and body["status"] not in _ALLOWED_STATUS:
        body.pop("status")
    if isinstance(body.get("flags"), list):
        body["flags"] = [
            {"reason": _esc(f.get("reason") or "Other", 200), "time": _esc(f.get("time"), 40)}
            for f in body["flags"][:10] if isinstance(f, dict)
        ]
    elif "flags" in body:
        body.pop("flags")
    for k in ("candidateFeedback", "jobMotivation"):
        if k in body:
            body[k] = str(body[k] or "")[:2000]
    if "helpMessages" in body:
        known = {_msg_key(m) for m in (existing.get("helpMessages") or [])}
        clean = []
        for m in (body["helpMessages"] if isinstance(body["helpMessages"], list) else [])[:200]:
            # Candidates can only author candidate messages; admin replies already live on the
            # server (the candidate's local copy of them must not be re-added as candidate posts).
            if not isinstance(m, dict) or m.get("from") == "admin":
                continue
            photo = m.get("photo")
            if not (isinstance(photo, str) and photo.startswith("data:image/") and len(photo) < 4_000_000
                    and not re.search(r'["\'<>\s]', photo)):
                photo = None
            item = {"from": "candidate", "text": _esc(m.get("text"), 500),
                    "at": _esc(m.get("at"), 40), "photo": photo}
            if _msg_key(item) in known:
                continue  # already stored
            clean.append(item)
        body["helpMessages"] = clean
    return body


def _msg_key(m):
    if not isinstance(m, dict):
        return json.dumps(m, sort_keys=True, default=str)
    return (m.get("from"), m.get("at"), m.get("text"))


def _union_messages(a, b):
    out, seen = [], set()
    for m in list(a or []) + list(b or []):
        k = _msg_key(m)
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    out.sort(key=lambda m: (m.get("at") or "") if isinstance(m, dict) else "")
    return out


def merge_assessment(existing, body, is_admin):
    """Single source of truth for merging a PUT into a stored record (DB and file mode used
    to have two diverging copies of this logic)."""
    body = dict(body)
    if not is_admin:
        for k in CANDIDATE_PROTECTED:
            body.pop(k, None)
    merged = dict(existing)
    for k, v in body.items():
        if k in ("photoHistory", "videoHistory") and not v and existing.get(k):
            continue
        if k == "score" and (v is None or v == "") and existing.get("score") is not None:
            continue
        if k == "completedAt" and not v and existing.get("completedAt"):
            continue
        if k in ("answers", "flags", "helpMessages"):
            continue  # handled below
        merged[k] = v

    # answers: never let a stale/partial sync wipe or roll back saved answers
    ea = existing.get("answers") if isinstance(existing.get("answers"), dict) else {}
    ba = body.get("answers") if isinstance(body.get("answers"), dict) else None
    if ba is not None:
        if not ba and ea:
            merged["answers"] = ea
        elif is_admin or (existing.get("status") == "completed"):
            merged["answers"] = {**ba, **ea}  # existing wins; new keys still added
        else:
            merged["answers"] = ba

    # help chat: union so neither side's message can be dropped by a stale copy
    if "helpMessages" in body:
        merged["helpMessages"] = _union_messages(existing.get("helpMessages"), body.get("helpMessages"))

    # flags. HR "frees" a candidate by clearing flags, but the candidate's page keeps re-sending
    # its old local flags every few seconds and would silently re-flag them. So when HR removes
    # flags we remember exactly which ones (by time+reason, not by clock comparison, so device
    # clock drift can't matter) and drop them if a candidate sends them again.
    fkey = lambda f: ("%s|%s" % (f.get("time"), f.get("reason"))) if isinstance(f, dict) else str(f)
    ef = existing.get("flags") if isinstance(existing.get("flags"), list) else []
    if "flags" in body and isinstance(body["flags"], list):
        bf = body["flags"]
        if is_admin:
            merged["flags"] = bf
            kept = {fkey(f) for f in bf}
            removed = [fkey(f) for f in ef if fkey(f) not in kept]
            if removed:
                merged["flagsCleared"] = (list(existing.get("flagsCleared") or []) + removed)[-60:]
        else:
            cleared = set(existing.get("flagsCleared") or [])
            have = {fkey(f) for f in ef}
            combined = list(ef)
            for f in bf:
                k = fkey(f)
                if k in cleared or k in have:
                    continue
                combined.append(f)
                have.add(k)
            merged["flags"] = combined[:3]
            if (merged.get("status") == "flagged" and len(merged["flags"]) < 3
                    and existing.get("status") != "completed"):
                merged["status"] = "in-progress"

    # completed is sticky
    if body.get("status") == "completed" and (is_admin or existing.get("status") != "completed"):
        merged["status"] = "completed"
        if body.get("score") is not None:
            merged["score"] = body.get("score")
        if body.get("completedAt"):
            merged["completedAt"] = body.get("completedAt")
    if existing.get("status") == "completed":
        if merged.get("status") in ("pending", "in-progress", "expired", "missed", "flagged"):
            merged["status"] = "completed"
        if existing.get("score") is not None and merged.get("score") is None:
            merged["score"] = existing.get("score")
        if existing.get("completedAt") and not merged.get("completedAt"):
            merged["completedAt"] = existing.get("completedAt")
        if not is_admin:
            for k in FROZEN_AFTER_COMPLETE:
                if k in existing:
                    merged[k] = existing[k]
    merged["id"] = existing.get("id", merged.get("id"))
    return merged


def upsert_assessment(aid, body, merge_existing=True, is_admin=True):
    """Insert or update ONE assessment, atomically (row lock in DB mode, so the candidate's
    answer-sync and photo upload can't overwrite each other's read-modify-write)."""
    if USE_DB:
        with pg(tx=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT payload FROM assessments WHERE id=%s FOR UPDATE", (aid,))
            row = cur.fetchone()
            if row:
                existing = _payload(row[0])
                if merge_existing:
                    merged = merge_assessment(existing, body, is_admin)
                else:
                    merged = dict(body)
                    merged["id"] = aid
                cur.execute(
                    "UPDATE assessments SET payload=%s::jsonb, status=%s, name=%s, email=%s, updated_at=NOW() WHERE id=%s",
                    (json.dumps(merged), merged.get("status"), merged.get("name"), merged.get("email"), aid),
                )
            else:
                merged = dict(body)
                merged["id"] = aid
                cur.execute(
                    "INSERT INTO assessments (id, payload, status, name, email) VALUES (%s,%s::jsonb,%s,%s,%s) "
                    "ON CONFLICT (id) DO UPDATE SET payload=EXCLUDED.payload, status=EXCLUDED.status, "
                    "name=EXCLUDED.name, email=EXCLUDED.email, updated_at=NOW()",
                    (aid, json.dumps(merged), merged.get("status"), merged.get("name"), merged.get("email")),
                )
            cur.close()
        return merged
    with _file_lock:
        data = load_assessments()
        for i, a in enumerate(data):
            if a.get("id") == aid:
                if merge_existing:
                    merged = merge_assessment(a, body, is_admin)
                else:
                    merged = dict(body)
                    merged["id"] = aid
                data[i] = merged
                save_assessments(data)
                return merged
        item = dict(body)
        item["id"] = aid
        data.append(item)
        save_assessments(data)
        return item


def load_admin():
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("SELECT username, password, role FROM admin_users")
            rows = cur.fetchall()
            cur.close()
        return {"users": [{"user": r[0], "pass": r[1], "role": r[2]} for r in rows]}
    with _file_lock:
        ensure_data()
        with open(ADMIN_FILE, "r") as f:
            return json.load(f)


def save_admin(cred):
    _users_cache["at"] = 0  # force re-read so removed users/roles take effect immediately here
    if USE_DB:
        with pg(tx=True) as conn:  # one transaction: no window where zero users exist
            cur = conn.cursor()
            cur.execute("DELETE FROM admin_users")
            for u in cred.get("users", []):
                cur.execute(
                    "INSERT INTO admin_users (username, password, role) VALUES (%s,%s,%s)",
                    (u.get("user"), u.get("pass"), u.get("role", "coordinator")),
                )
            cur.close()
        return
    with _file_lock:
        tmp = ADMIN_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(cred, f, indent=2)
        os.replace(tmp, ADMIN_FILE)


# ---------- Settings (question bank overrides) ----------
def load_settings():
    if USE_DB:
        with pg() as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM settings WHERE key=%s", ("question_overrides",))
            row = cur.fetchone()
            cur.close()
        return (_payload(row[0]) or {}) if row else {}
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def update_settings(fn):
    """Atomic read-modify-write of the overrides blob (two admins saving different
    role/levels at once used to clobber each other)."""
    if USE_DB:
        with pg(tx=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT value FROM settings WHERE key=%s FOR UPDATE", ("question_overrides",))
            row = cur.fetchone()
            data = (_payload(row[0]) or {}) if row else {}
            fn(data)
            cur.execute(
                "INSERT INTO settings (key, value, updated_at) VALUES (%s, %s::jsonb, NOW()) "
                "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()",
                ("question_overrides", json.dumps(data)),
            )
            cur.close()
        return data
    with _file_lock:
        data = load_settings()
        fn(data)
        os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
        tmp = SETTINGS_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, SETTINGS_FILE)
        return data


MAX_PHOTO_CHARS = 4_000_000
MAX_VIDEO_CHARS = 30_000_000


def append_media(aid, kind, data_url, meta=None):
    """Store photo/video. Runs under a row lock so it can't race the answer-sync PUT."""
    meta = meta or {}
    at = meta.get("at") or datetime.utcnow().isoformat()
    if USE_DB:
        with pg(tx=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT payload FROM assessments WHERE id=%s FOR UPDATE", (aid,))
            row = cur.fetchone()
            if not row:
                cur.close()
                return None, "Not found"
            payload = _payload(row[0])
            cur.execute(
                "INSERT INTO assessment_media (assessment_id, kind, data, meta) VALUES (%s,%s,%s,%s::jsonb) RETURNING id",
                (aid, kind, data_url, json.dumps(meta)),
            )
            mid = cur.fetchone()[0]
            if kind == "photo":
                hist = payload.get("photoHistory") or []
                hist.append({"img": data_url, "at": at, "mediaId": mid})
                # Embedded preview cap; the FULL set is always kept in assessment_media.
                if len(hist) > 1000:
                    hist = hist[-1000:]
                payload["photoHistory"] = hist
                payload["lastPhoto"] = data_url
                payload["lastPhotoAt"] = at
            else:
                hist = payload.get("videoHistory") or []
                hist.append({"video": data_url, "at": at, "seconds": meta.get("seconds", 15), "mediaId": mid})
                if len(hist) > 10:
                    hist = hist[-10:]
                payload["videoHistory"] = hist
                payload["lastVideoAt"] = at
            cur.execute(
                "UPDATE assessments SET payload=%s::jsonb, updated_at=NOW() WHERE id=%s",
                (json.dumps(payload), aid),
            )
            cur.close()
        return payload, None
    with _file_lock:
        data = load_assessments()
        for i, a in enumerate(data):
            if a.get("id") == aid:
                if kind == "photo":
                    hist = a.get("photoHistory") or []
                    hist.append({"img": data_url, "at": at})
                    if len(hist) > 1000:
                        hist = hist[-1000:]
                    a["photoHistory"] = hist
                    a["lastPhoto"] = data_url
                    a["lastPhotoAt"] = at
                else:
                    hist = a.get("videoHistory") or []
                    hist.append({"video": data_url, "at": at, "seconds": meta.get("seconds", 15)})
                    if len(hist) > 20:
                        hist = hist[-20:]
                    a["videoHistory"] = hist
                    a["lastVideoAt"] = at
                data[i] = a
                save_assessments(data)
                return a, None
        return None, "Not found"


def clear_media(aid):
    """Delete photos/videos for one candidate; keep scores/answers/flags."""
    def wipe(p):
        p["photoHistory"] = []
        p["videoHistory"] = []
        p["lastPhoto"] = None
        p["lastPhotoAt"] = None
        p["lastVideoAt"] = None
        p["photoCount"] = 0
    if USE_DB:
        with pg(tx=True) as conn:
            cur = conn.cursor()
            cur.execute("SELECT payload FROM assessments WHERE id=%s FOR UPDATE", (aid,))
            row = cur.fetchone()
            if not row:
                cur.close()
                return False
            cur.execute("DELETE FROM assessment_media WHERE assessment_id=%s", (aid,))
            payload = _payload(row[0])
            wipe(payload)
            cur.execute("UPDATE assessments SET payload=%s::jsonb, updated_at=NOW() WHERE id=%s",
                        (json.dumps(payload), aid))
            cur.close()
        return True
    with _file_lock:
        data = load_assessments()
        for i, a in enumerate(data):
            if a.get("id") == aid:
                wipe(a)
                data[i] = a
                save_assessments(data)
                return True
        return False


# ---------- Auth ----------
# Tokens are now stateless HMAC-signed strings. They used to live in an in-memory dict, but
# Procfile runs 2 gunicorn workers: a login handled by worker A was unknown to worker B, so
# roughly every other admin request came back 401 "please log in again" (and every restart
# logged everyone out).
TOKEN_TTL_SECONDS = 12 * 60 * 60


def _secret():
    env = os.environ.get("SECRET_KEY", "").strip()
    if env:
        return env.encode()
    if USE_DB:
        return hashlib.sha256(("qrs-token-v1|" + DATABASE_URL).encode()).digest()
    path = os.path.join(BASE, "data", ".secret")
    with _file_lock:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Two gunicorn workers boot at the same time: create the file atomically (O_EXCL) so
        # only ONE key is ever written. The old exists()+write() race let each worker sign
        # with a different key, so about half of all admin requests came back 401.
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "w") as f:
                f.write(secrets.token_hex(32))
        except FileExistsError:
            pass
        for _ in range(20):  # the winner may not have finished writing yet
            with open(path) as f:
                val = f.read().strip()
            if len(val) >= 32:
                return val.encode()
            time.sleep(0.05)
        return hashlib.sha256(("qrs-token-fallback|" + BASE).encode()).digest()


_SECRET_CACHE = None


def _sign(msg):
    global _SECRET_CACHE
    if _SECRET_CACHE is None:
        _SECRET_CACHE = _secret()
    return base64.urlsafe_b64encode(hmac.new(_SECRET_CACHE, msg.encode(), hashlib.sha256).digest()).decode().rstrip("=")


def issue_token(user, role):
    body = base64.urlsafe_b64encode(json.dumps(
        {"u": user, "r": role, "e": int(time.time() + TOKEN_TTL_SECONDS)}).encode()).decode().rstrip("=")
    return "qrs1." + body + "." + _sign(body)


_users_cache = {"at": 0, "map": {}}


def _users_map():
    """username -> role, cached 10s so deleted users / role changes take effect quickly
    without a DB hit on every request."""
    if time.time() - _users_cache["at"] > 10:
        try:
            users = load_admin().get("users", [])
            _users_cache["map"] = {u.get("user"): u.get("role", "coordinator") for u in users}
            _users_cache["at"] = time.time()
        except Exception as e:
            print("users cache refresh failed:", e)
    return _users_cache["map"]


def current_admin():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[len("Bearer "):].strip()
    try:
        tag, body, sig = token.split(".")
        if tag != "qrs1" or not hmac.compare_digest(sig, _sign(body)):
            return None
        data = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    except Exception:
        return None
    if data.get("e", 0) < time.time():
        return None
    role = _users_map().get(data.get("u"))
    if role is None:
        return None  # user was deleted
    return {"user": data["u"], "role": role, "exp": data["e"]}


def _check_pw(stored, supplied):
    if not stored or supplied is None:
        return False
    supplied = str(supplied)
    if stored.startswith(("pbkdf2:", "scrypt:")):
        return check_password_hash(stored, supplied)
    return hmac.compare_digest(str(stored).encode(), supplied.encode())  # legacy plaintext


_LOGIN_FAILS = {}


def _login_throttled(key):
    now = time.time()
    fails = [t for t in _LOGIN_FAILS.get(key, []) if now - t < 600]
    _LOGIN_FAILS[key] = fails
    return len(fails) >= 8


def json_body():
    """Always a dict (get_json(force=True) or {} crashed with 500 on a JSON list/garbage)."""
    body = request.get_json(force=True, silent=True)
    return body if isinstance(body, dict) else {}


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_admin():
            return jsonify({"ok": False, "error": "Unauthorized — please log in again"}), 401
        return fn(*args, **kwargs)

    return wrapper


def require_primary_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        rec = current_admin()
        if not rec:
            return jsonify({"ok": False, "error": "Unauthorized — please log in again"}), 401
        if rec.get("role") != "admin":
            return jsonify({"ok": False, "error": "Only the primary admin can manage team accounts"}), 403
        return fn(*args, **kwargs)

    return wrapper


def candidate_token_ok(record, supplied_token):
    a, b = record.get("token"), supplied_token
    if not a or not b or not isinstance(b, str):
        return False
    return hmac.compare_digest(str(a).encode(), b.encode())


@app.after_request
def _headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    # candidate links carry ?token=... — don't leak it via the Referer header
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    if request.path.startswith("/api/"):
        resp.headers["Cache-Control"] = "no-store"
    return resp


def parse_iso_utc_naive(ts):
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return dt.replace(tzinfo=None)
    except Exception:
        return None


def is_link_expired(a):
    """True only when past expiresAt (+ 10 min grace). Rebuild from linkValidFrom + hours if needed."""
    from datetime import timedelta
    exp = parse_iso_utc_naive(a.get("expiresAt"))
    hours = a.get("linkValidityHours") or 24
    try:
        hours = int(hours)
    except Exception:
        hours = 24
    start = parse_iso_utc_naive(a.get("linkValidFrom")) or parse_iso_utc_naive(a.get("scheduledAt")) or parse_iso_utc_naive(a.get("createdAt"))
    if start:
        rebuilt = start + timedelta(hours=hours)
        if exp is None or rebuilt > exp:
            exp = rebuilt
    if not exp:
        return False
    return datetime.utcnow() > (exp + timedelta(minutes=10))


# ---------- Email (SMTP) ----------
# Works with Gmail (use an App Password, not your normal password), Outlook/Office365,
# or any SMTP provider. Configure these as environment variables on your host — nothing
# is hardcoded, and if they're not set, sending is simply disabled (manual "Copy Link" /
# "Email Link" in admin.html still always works regardless).
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587") or "587")
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM_NAME = os.environ.get("SMTP_FROM_NAME", "QRS Assessments")
SMTP_FROM_EMAIL = os.environ.get("SMTP_FROM_EMAIL", "") or SMTP_USER
EMAIL_CONFIGURED = bool(SMTP_HOST and SMTP_USER and SMTP_PASS and SMTP_FROM_EMAIL)


def send_email(to_email, subject, html_body):
    """Send one email over SMTP. Returns (ok: bool, error: str|None)."""
    if not EMAIL_CONFIGURED:
        return False, "Email sending is not configured on this server (SMTP_HOST/USER/PASS env vars are missing)."
    if not to_email or "@" not in to_email:
        return False, "Candidate has no valid email address on file."
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.utils import formataddr

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((SMTP_FROM_NAME, SMTP_FROM_EMAIL))
        msg["To"] = to_email
        # "No-reply" convention: tell the recipient's mail client not to thread replies here.
        msg["Reply-To"] = SMTP_FROM_EMAIL
        msg.attach(MIMEText(html_body, "html"))

        if SMTP_PORT == 465:
            server_cm = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
        else:
            server_cm = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
        with server_cm as server:
            if SMTP_PORT != 465:
                server.ehlo()
                server.starttls()
                server.ehlo()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM_EMAIL, [to_email], msg.as_string())
        return True, None
    except Exception as e:
        print("Email send failed:", e)
        return False, str(e)


def build_link_email_html(name, role, level, link, duration, expires_at_str, unlock_at_str=None, validity_hours=None):
    e = lambda v: _html.escape(str(v if v is not None else ""), quote=True)
    name, link = e(name), e(link)
    unlock_at_str = e(unlock_at_str) if unlock_at_str else None
    start_line = (
        f"The assessment will start on <strong>{unlock_at_str}</strong>."
        if unlock_at_str else
        "The assessment is available to start right away."
    )
    validity_hours_str = e(validity_hours or 24)
    return f"""
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:520px;margin:0 auto;color:#0f172a;">
      <div style="background:#0f172a;padding:1.2rem 1.5rem;border-radius:12px 12px 0 0;">
        <span style="color:#fff;font-weight:700;font-size:1.05rem;">QRS Solutions — Assessment Round</span>
      </div>
      <div style="border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;padding:1.5rem;">
        <p>Hi {name},</p>
        <p><strong>Congratulations!</strong> You have been shortlisted for the Assessment Round.</p>
        <p>{start_line} Kindly attend the test without fail and ensure that you:</p>
        <ul style="font-size:0.9rem;color:#334155;">
          <li>Attend the test using a laptop.</li>
          <li>Sit in a quiet and well-lit place.</li>
          <li>Have a stable internet connection.</li>
          <li>Complete the assessment within the given time.</li>
        </ul>
        <p style="margin:1.3rem 0;text-align:center;">
          <a href="{link}" style="background:#4f46e5;color:#fff;text-decoration:none;font-weight:600;padding:0.75rem 1.5rem;border-radius:10px;display:inline-block;">Start Assessment</a>
        </p>
        <p style="font-size:0.85rem;color:#64748b;word-break:break-all;">Assessment Link: {link}</p>
        <p style="font-size:0.88rem;color:#334155;"><strong>Important:</strong> The assessment link will be valid for {validity_hours_str} hours from the scheduled assessment start time. Please ensure that you access and complete the assessment within the validity period.</p>
        <p style="margin-top:1.3rem;">Best wishes for your assessment!</p>
        <p style="font-size:0.85rem;color:#94a3b8;margin-top:1rem;">This is an automated message — please do not reply to this email. If you have questions, contact your recruiter directly.</p>
      </div>
    </div>
    """


@app.route("/api/assessments/<aid>/send-link", methods=["POST"])
@require_admin
def send_link_email(aid):
    """Email a candidate their test link. Admin/coordinator only — admin.html supplies
    the fully-built link since only the frontend knows its own public URL."""
    body = json_body()
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    to_email = body.get("email") or a.get("email")
    link = body.get("link")
    if not link:
        return jsonify({"ok": False, "error": "Missing link"}), 400
    if not re.match(r"^https?://", str(link)):
        return jsonify({"ok": False, "error": "Link must start with http:// or https://"}), 400
    subject = body.get("subject") or f"Congratulations! Your QRS 2nd Round Assessment Link — {a.get('role','')}"
    html = build_link_email_html(
        name=a.get("name", "Candidate"),
        role=a.get("role", ""),
        level=a.get("level", ""),
        link=link,
        duration=body.get("duration") or a.get("duration") or "—",
        expires_at_str=body.get("expiresAtLabel") or a.get("expiresAt") or "—",
        unlock_at_str=body.get("unlockAtLabel"),
        validity_hours=body.get("validityHours") or a.get("linkValidityHours"),
    )
    ok, err = send_email(to_email, subject, html)
    if ok:
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": err}), 500


def build_result_card_email_html(a, total, pass_mark=60):
    """Professional result summary for the candidate (no internal HR notes)."""
    _e = lambda v: _html.escape(str(v), quote=True)
    name = _e(a.get("name") or "Candidate")
    role = _e((a.get("role") or "—").replace("_", " ").title())
    level = _e((a.get("level") or "—").title())
    status = _e(a.get("status") or "—")
    mcq = a.get("score")
    final = a.get("finalScore")
    score_show = total if total is not None else (final if final is not None else mcq)
    try:
        score_show = int(score_show) if score_show is not None and score_show != "" else None
    except Exception:
        score_show = None
    result_label = ""
    if score_show is not None:
        result_label = "Pass" if score_show >= pass_mark else "Under review"
    completed = a.get("completedAt") or ""
    try:
        if completed:
            completed = datetime.fromisoformat(str(completed).replace("Z", "+00:00")).strftime("%d %b %Y, %I:%M %p")
    except Exception:
        pass
    score_html = f"<div style='font-size:2rem;font-weight:700;color:#4f46e5;margin:0.5rem 0;'>{score_show} / 100</div>" if score_show is not None else "<div style='color:#64748b;margin:0.5rem 0;'>Score will be shared after review</div>"
    result_html = f"<p style='margin:0.25rem 0;font-size:0.95rem;'><strong>Outcome:</strong> {result_label}</p>" if result_label else ""
    return f"""
    <div style="font-family:Arial,Helvetica,sans-serif;max-width:520px;margin:0 auto;color:#0f172a;">
      <div style="background:#0f172a;padding:1.2rem 1.5rem;border-radius:12px 12px 0 0;">
        <span style="color:#fff;font-weight:700;font-size:1.05rem;">QRS Solutions — Assessment Result</span>
      </div>
      <div style="border:1px solid #e2e8f0;border-top:none;border-radius:0 0 12px 12px;padding:1.5rem;">
        <p>Hi {name},</p>
        <p>Thank you for completing the <strong>QRS second-round assessment</strong>.</p>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:1rem 1.15rem;margin:1rem 0;">
          <div style="font-size:0.8rem;color:#64748b;text-transform:uppercase;letter-spacing:0.04em;font-weight:700;">Result card</div>
          {score_html}
          <p style="margin:0.25rem 0;font-size:0.95rem;"><strong>Role:</strong> {role} · {level}</p>
          <p style="margin:0.25rem 0;font-size:0.95rem;"><strong>Status:</strong> {status}</p>
          {result_html}
          <p style="margin:0.25rem 0;font-size:0.9rem;color:#64748b;">Completed: {completed or "—"}</p>
        </div>
        <p>Our team will contact you regarding the next steps. If you have questions, please reply to your recruiter.</p>
        <p style="margin-top:1.2rem;">Best regards,<br><strong>QRS Recruitment Team</strong></p>
        <p style="font-size:0.8rem;color:#94a3b8;margin-top:1rem;">This is an automated message from the QRS Assessment Portal.</p>
      </div>
    </div>
    """


@app.route("/api/assessments/<aid>/send-result", methods=["POST"])
@require_admin
def send_result_email(aid):
    """Email a candidate their result card. Uses free SMTP if configured (e.g. Gmail App Password)."""
    body = json_body()
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    to_email = body.get("email") or a.get("email")
    if not to_email or "@" not in str(to_email):
        return jsonify({"ok": False, "error": "Candidate has no email on file"}), 400
    # Prefer final score, else MCQ + coding + voice style total from client if provided
    total = body.get("totalScore")
    if total is None:
        if a.get("finalScore") is not None and a.get("finalScore") != "":
            total = a.get("finalScore")
        else:
            total = a.get("score")
    try:
        pass_mark = int(body.get("passMark") or 60)
    except Exception:
        pass_mark = 60
    subject = body.get("subject") or f"Your QRS Assessment Result — {a.get('name') or 'Candidate'}"
    html = build_result_card_email_html(a, total, pass_mark=pass_mark)
    if not EMAIL_CONFIGURED:
        return jsonify({
            "ok": False,
            "error": "Email not configured. Set SMTP_HOST, SMTP_USER, SMTP_PASS on Render (free Gmail App Password works).",
            "email_configured": False,
            "mailto_subject": subject,
            "mailto_hint": True,
        }), 503
    ok, err = send_email(to_email, subject, html)
    if ok:
        return jsonify({"ok": True, "to": to_email})
    return jsonify({"ok": False, "error": err}), 500


# ---------- Routes ----------
@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/<path:name>")
def static_whitelist(name):
    """Only the front-end files are public; everything else (backend.py, data/, .env ...) is 404."""
    if name in STATIC_FILES:
        return send_from_directory(BASE, name)
    abort(404)


@app.route("/api/assessments/<aid>/result-card", methods=["POST"])
@require_admin
def create_result_card_link(aid):
    """HR generates a candidate-facing result card link (valid 5 hours). Reveals only after review."""
    body = json_body()
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    # Require HR review before reveal
    has_final = a.get("finalScore") is not None and a.get("finalScore") != ""
    force = bool(body.get("force"))
    if not has_final and not force:
        return jsonify({
            "ok": False,
            "error": "Save a final score in the Review panel first — then the result card can be revealed to the candidate.",
        }), 400
    from datetime import timedelta
    hours = 5
    try:
        hours = int(body.get("hours") or 5)
    except Exception:
        hours = 5
    hours = max(1, min(48, hours))
    token = secrets.token_urlsafe(16)
    now = datetime.utcnow()
    expires = now + timedelta(hours=hours)
    patch = {
        "resultCardToken": token,
        "resultCardCreatedAt": now.isoformat() + "Z",
        "resultCardExpiresAt": expires.isoformat() + "Z",
        "resultCardRevealed": True,
        "resultCardHours": hours,
    }
    saved = upsert_assessment(aid, patch, merge_existing=True)
    return jsonify({
        "ok": True,
        "id": aid,
        "token": token,
        "expiresAt": patch["resultCardExpiresAt"],
        "hours": hours,
        "revealed": True,
    })


@app.route("/api/result-card/<aid>", methods=["GET"])
def public_result_card(aid):
    """Public candidate view — limited fields only. Requires result card token."""
    token = (request.args.get("token") or "").strip()
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    if not token or not hmac.compare_digest(token.encode(), str(a.get("resultCardToken") or "").encode()):
        return jsonify({"ok": False, "error": "Invalid or missing result card link"}), 401
    # Expiry check
    exp = parse_iso_utc_naive(a.get("resultCardExpiresAt"))
    if exp and datetime.utcnow() > exp:
        return jsonify({
            "ok": False,
            "error": "This result card link has expired (valid for a limited time after HR review).",
            "expired": True,
        }), 410
    if not a.get("resultCardRevealed"):
        return jsonify({
            "ok": False,
            "error": "Your result is not available yet. HR is still reviewing your assessment.",
            "pending": True,
        }), 403

    # Score: prefer final
    score = a.get("finalScore")
    if score is None or score == "":
        score = a.get("score")
    try:
        score = int(score) if score is not None and score != "" else None
    except Exception:
        score = None

    # Time taken
    started = parse_iso_utc_naive(a.get("startedAt"))
    completed = parse_iso_utc_naive(a.get("completedAt"))
    minutes = None
    if started and completed and completed > started:
        minutes = int(round((completed - started).total_seconds() / 60.0))

    flags_count = len(a.get("flags") or [])

    # Strength from coding effort or score bands
    strength = a.get("codingEffort") or ""
    if not strength and score is not None:
        if score >= 80:
            strength = "Strong"
        elif score >= 60:
            strength = "Good"
        elif score >= 40:
            strength = "Developing"
        else:
            strength = "Needs improvement"
    if not strength:
        strength = "Under review"

    # Never expose internal notes, answers, photos, flag reasons
    hr_reply = ""
    if a.get("hrReplyShareOnCard") and a.get("hrReplyToNote"):
        hr_reply = str(a.get("hrReplyToNote") or "")[:2000]
    payload = {
        "ok": True,
        "name": a.get("name") or "Candidate",
        "role": a.get("role") or "",
        "level": a.get("level") or "",
        "status": a.get("status") or "",
        "score": score,
        "flagsCount": flags_count,
        "timeTakenMinutes": minutes,
        "startedAt": a.get("startedAt"),
        "finishedAt": a.get("completedAt"),
        "strength": strength,
        "expiresAt": a.get("resultCardExpiresAt"),
        "revealed": True,
        "hrReply": hr_reply,  # only if HR opted to share on card
    }
    return jsonify(payload)




@app.route("/api/health")
def health():
    storage = "postgres" if USE_DB else "json-file"
    count = 0
    try:
        count = count_assessments()
    except Exception as e:
        print("health check failed:", e)
        return jsonify({"ok": False, "storage": storage, "error": "storage unavailable (" + type(e).__name__ + ")"}), 500
    return jsonify(
        {
            "ok": True,
            "backend": "flask",
            "storage": storage,
            "candidates": count,
            "email_configured": EMAIL_CONFIGURED,
            "time": datetime.utcnow().isoformat() + "Z",
        }
    )


# ---------- Question Bank overrides (in-admin editor) ----------
@app.route("/api/questions", methods=["GET"])
def list_question_overrides():
    """Public — test.html needs this for every candidate, not just admins."""
    return jsonify({"overrides": load_settings()})


_KEY_RE = re.compile(r"^[A-Za-z0-9_\- ]{1,40}$")


@app.route("/api/questions/<role>/<level>", methods=["PUT"])
def put_question_override(role, level):
    admin = current_admin()
    if not admin:
        return jsonify({"error": "Unauthorized"}), 401
    if not (_KEY_RE.match(role) and _KEY_RE.match(level)):
        return jsonify({"error": "Invalid role/level"}), 400
    body = json_body()
    questions = body.get("questions")
    if not isinstance(questions, list) or not questions:
        return jsonify({"error": "questions must be a non-empty list"}), 400
    total_marks = 0
    for i, q in enumerate(questions):
        if not isinstance(q, dict):
            return jsonify({"error": f"Question #{i+1} is not an object"}), 400
        if not q.get("id") or not q.get("type") or not q.get("question"):
            return jsonify({"error": f"Question #{i+1} is missing id/type/question"}), 400
        if q.get("type") == "mcq" and (not q.get("options") or q.get("correct") is None):
            return jsonify({"error": f"Question #{i+1} (MCQ) needs options and a correct answer"}), 400
        try:
            total_marks += int(float(q.get("marks") or 0))
        except (TypeError, ValueError):
            return jsonify({"error": f"Question #{i+1} has a non-numeric marks value"}), 400
    try:
        duration = max(1, min(600, int(float(body.get("duration") or 45))))
    except (TypeError, ValueError):
        duration = 45
    key = f"{role.lower()}/{level.lower()}"

    def apply(overrides):
        overrides[key] = {
            "duration": duration,
            "questions": questions,
            "totalMarks": total_marks,
            "updatedAt": datetime.utcnow().isoformat(),
            "updatedBy": admin.get("user", "admin"),
        }
    update_settings(apply)
    return jsonify({"ok": True, "totalMarks": total_marks})


@app.route("/api/questions/<role>/<level>", methods=["DELETE"])
def delete_question_override(role, level):
    """Revert a role/level back to the bundled questions.js defaults."""
    if not current_admin():
        return jsonify({"error": "Unauthorized"}), 401
    key = f"{role.lower()}/{level.lower()}"
    update_settings(lambda o: o.pop(key, None))
    return jsonify({"ok": True})


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = json_body()
    user, pw = body.get("user"), body.get("pass")
    key = (client_ip() or "?") + "|" + str(user)[:60]
    if _login_throttled(key):
        return jsonify({"ok": False, "error": "Too many failed attempts. Try again in 10 minutes."}), 429
    cred = load_admin()
    users = cred.get("users", [])
    match = next((u for u in users if u.get("user") == user and _check_pw(u.get("pass"), pw)), None)
    if match:
        _LOGIN_FAILS.pop(key, None)
        # transparently upgrade legacy plaintext passwords to hashes
        if not str(match.get("pass", "")).startswith(("pbkdf2:", "scrypt:")):
            try:
                match["pass"] = generate_password_hash(str(pw))
                save_admin(cred)
            except Exception as e:
                print("password hash upgrade failed:", e)
        role = match.get("role", "coordinator")
        token = issue_token(match["user"], role)
        return jsonify({"ok": True, "token": token, "user": match["user"], "role": role})
    _LOGIN_FAILS.setdefault(key, []).append(time.time())
    return jsonify({"ok": False, "error": "Invalid username or password"}), 401


@app.route("/api/admin/password", methods=["POST"])
@require_admin
def admin_password():
    body = json_body()
    new_pass = body.get("pass") or ""
    if not isinstance(new_pass, str) or len(new_pass) < 6:
        return jsonify({"ok": False, "error": "Password min 6 chars"}), 400
    rec = current_admin()
    cred = load_admin()
    for u in cred.get("users", []):
        if u.get("user") == rec["user"]:
            u["pass"] = generate_password_hash(new_pass)
            save_admin(cred)
            return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "User not found"}), 404


@app.route("/api/admin/users", methods=["GET"])
@require_admin
def list_users():
    cred = load_admin()
    users = [{"user": u.get("user"), "role": u.get("role", "coordinator")} for u in cred.get("users", [])]
    return jsonify(users)


@app.route("/api/admin/users", methods=["POST"])
@require_primary_admin
def add_user():
    body = json_body()
    username = str(body.get("user") or "").strip()
    password = body.get("pass") or ""
    if not username or not isinstance(password, str) or len(password) < 6:
        return jsonify({"ok": False, "error": "Username required, password min 6 chars"}), 400
    cred = load_admin()
    users = cred.get("users", [])
    if any(u.get("user") == username for u in users):
        return jsonify({"ok": False, "error": "That username already exists"}), 400
    users.append({"user": username, "pass": generate_password_hash(password), "role": "coordinator"})
    cred["users"] = users
    save_admin(cred)
    return jsonify({"ok": True}), 201


@app.route("/api/admin/users/<username>", methods=["DELETE"])
@require_primary_admin
def delete_user(username):
    if username == "admin":
        return jsonify({"ok": False, "error": "Cannot remove the primary admin account"}), 400
    cred = load_admin()
    users = cred.get("users", [])
    new_users = [u for u in users if u.get("user") != username]
    if len(new_users) == len(users):
        return jsonify({"ok": False, "error": "User not found"}), 404
    cred["users"] = new_users
    save_admin(cred)  # their existing tokens stop working immediately (see current_admin)
    return jsonify({"ok": True})


@app.route("/api/assessments", methods=["GET"])
@require_admin
def list_assessments():
    return jsonify(load_assessments())


@app.route("/api/assessments", methods=["POST"])
@require_admin
def create_assessment():
    body = json_body()
    item = {
        "id": body.get("id") or ("QRS-" + uuid.uuid4().hex[:8].upper()),
        "token": body.get("token") or uuid.uuid4().hex,
        "name": body.get("name", ""),
        "email": body.get("email", ""),
        "mobile": body.get("mobile", ""),
        "role": body.get("role", ""),
        "level": body.get("level", ""),
        "status": body.get("status", "pending"),
        "score": body.get("score"),
        "voiceScore": body.get("voiceScore"),
        "flags": body.get("flags") or [],
        "answers": body.get("answers") or {},
        "createdAt": body.get("createdAt") or datetime.utcnow().isoformat(),
        "startedAt": body.get("startedAt"),
        "completedAt": body.get("completedAt"),
        "extraMinutes": body.get("extraMinutes") or 0,
        "scheduledAt": body.get("scheduledAt"),
        "expiresAt": body.get("expiresAt"),
        "duration": body.get("duration"),
        "linkValidityHours": body.get("linkValidityHours"),
        "lastPhoto": body.get("lastPhoto"),
        "lastPhotoAt": body.get("lastPhotoAt"),
        "photoHistory": body.get("photoHistory") or [],
        "lastVideoAt": body.get("lastVideoAt"),
        "videoHistory": body.get("videoHistory") or [],
        "allowMobile": bool(body.get("allowMobile")),
        "storePhotos": body.get("storePhotos") if body.get("storePhotos") is not None else True,
        "linkValidFrom": body.get("linkValidFrom"),
        "totalMarks": body.get("totalMarks") or 100,
        "sessionId": body.get("sessionId"),
        "lastActivityAt": body.get("lastActivityAt"),
    }
    # single-row insert: this used to re-save EVERY candidate from a stale snapshot, which could
    # roll back a candidate's live answers/status and drop records created at the same moment
    if not insert_assessment(item):
        return jsonify({"ok": False, "error": "A record with this id already exists"}), 409
    return jsonify(item), 201


@app.route("/api/assessments/<aid>", methods=["GET"])
def get_assessment(aid):
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"error": "Not found"}), 404
    if current_admin():
        return jsonify(a)
    if candidate_token_ok(a, request.args.get("token")):
        # Candidates never see HR notes, final score, result-card token or proctoring media
        return jsonify({k: v for k, v in a.items() if k not in CANDIDATE_HIDDEN})
    return jsonify({"error": "Unauthorized"}), 401


def _sanitize_candidate_score_fields(body):
    """A candidate's own PUT is client JS the candidate's browser can be told to edit —
    the request body is not trustworthy. This does not re-grade the test (the backend has
    no copy of the correct answers to check against), but it stops an out-of-range or
    inconsistent value (e.g. a fabricated 100/100) from being written verbatim. Real
    protection requires scoring MCQs server-side against a backend copy of the question
    bank; this is a bounds check only.
    """
    def _num(v):
        try:
            n = float(v)
            return n if n == n and n not in (float("inf"), float("-inf")) else None  # reject NaN/inf
        except (TypeError, ValueError):
            return None

    mcq_total = _num(body.get("mcqTotal"))
    if mcq_total is not None:
        mcq_total = max(0, min(100, mcq_total))
        body["mcqTotal"] = mcq_total
    score_cap = mcq_total if mcq_total is not None else 100

    mcq_count = _num(body.get("mcqCount"))
    if mcq_count is not None:
        mcq_count = max(0, min(100, round(mcq_count)))
        body["mcqCount"] = mcq_count

    mcq_correct = _num(body.get("mcqCorrect"))
    if mcq_correct is not None:
        cap = mcq_count if mcq_count is not None else 100
        mcq_correct = max(0, min(cap, round(mcq_correct)))
        body["mcqCorrect"] = mcq_correct

    if "mcqScore" in body:
        v = _num(body.get("mcqScore"))
        body["mcqScore"] = 0 if v is None else max(0, min(score_cap, v))

    if "score" in body:
        v = _num(body.get("score"))
        body["score"] = 0 if v is None else max(0, min(score_cap, v))
    return body


@app.route("/api/assessments/<aid>", methods=["PUT"])
def update_assessment(aid):
    body = json_body()
    admin_rec = current_admin()
    existing = get_one_assessment(aid)
    if existing:
        if not admin_rec and not candidate_token_ok(existing, body.get("token")):
            return jsonify({"ok": False, "error": "Unauthorized"}), 401
        if not admin_rec:
            body = _sanitize_candidate_score_fields(body)
            body = sanitize_candidate_body(body, existing)
            for k in ("clientIp", "userAgent", "lastSeenIp"):
                body.pop(k, None)  # never trust client-supplied values
            body = attach_client_meta(body, existing)
            # A candidate starting/finishing a test that is still 'pending' after the link
            # expired is rejected here even if the browser-side check was bypassed.
            leaving_pending = body.get("status") in ("in-progress", "completed") and existing.get("status") == "pending"
            if leaving_pending and is_link_expired(existing):
                return jsonify({"ok": False, "error": "This link has expired."}), 403
        saved = upsert_assessment(aid, body, merge_existing=True, is_admin=bool(admin_rec))
        if not admin_rec:
            saved = {k: v for k, v in saved.items() if k not in CANDIDATE_HIDDEN}
        return jsonify(saved)
    if not admin_rec:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    item = upsert_assessment(aid, body, merge_existing=False)
    return jsonify(item), 201


def _add_media(aid, kind, field, max_chars, prefix):
    body = json_body()
    data = body.get(field)
    at = body.get("at") or datetime.utcnow().isoformat()
    if not data or not isinstance(data, str):
        return jsonify({"error": field + " required"}), 400
    if not data.startswith(prefix):
        return jsonify({"error": "invalid " + field + " data"}), 400
    if len(data) > max_chars:
        return jsonify({"error": field + " too large"}), 413
    existing = get_one_assessment(aid)
    if not existing:
        return jsonify({"error": "Not found"}), 404
    if not current_admin() and not candidate_token_ok(existing, body.get("token")):
        return jsonify({"error": "Unauthorized"}), 401
    meta = {"at": str(at)[:40]}
    if kind == "video":
        try:
            meta["seconds"] = int(body.get("seconds") or 15)
        except (TypeError, ValueError):
            meta["seconds"] = 15
    payload, err = append_media(aid, kind, data, meta)
    if err:
        return jsonify({"error": err}), 404
    hist = payload.get("photoHistory" if kind == "photo" else "videoHistory") or []
    return jsonify({"ok": True, "count": len(hist)})


@app.route("/api/assessments/<aid>/photos", methods=["POST"])
def add_photo(aid):
    return _add_media(aid, "photo", "img", MAX_PHOTO_CHARS, "data:image/")


@app.route("/api/assessments/<aid>/videos", methods=["POST"])
def add_video(aid):
    return _add_media(aid, "video", "video", MAX_VIDEO_CHARS, "data:video/")


@app.route("/api/assessments/<aid>/media", methods=["DELETE"])
@require_admin
def delete_media(aid):
    """Clear photos/videos after you finish review — keeps score, answers, flags."""
    if clear_media(aid):
        return jsonify({"ok": True, "cleared": aid})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/assessments/<aid>", methods=["DELETE"])
@require_admin
def delete_assessment(aid):
    if delete_one_assessment(aid):
        return jsonify({"ok": True, "deleted": aid})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/admin/restore", methods=["POST"])
@require_admin
def restore_bulk():
    """Upload a list of assessments (from Backup JSON) into storage. Row-by-row: the old
    version rewrote the whole table from a snapshot, racing live candidates."""
    raw = request.get_json(force=True, silent=True)
    items = raw if isinstance(raw, list) else ((raw or {}).get("assessments") or (raw or {}).get("data") or [])
    if not isinstance(items, list) or not items:
        return jsonify({"ok": False, "error": "Send a JSON array of assessments"}), 400
    restored = skipped = 0
    for a in items:
        if not isinstance(a, dict) or not a.get("id"):
            skipped += 1
            continue
        aid = str(a["id"])
        old = get_one_assessment(aid)
        # keep the finished copy if the server already has one and the upload isn't finished
        if old and old.get("status") == "completed" and a.get("status") != "completed":
            skipped += 1
            continue
        upsert_assessment(aid, a, merge_existing=False)
        restored += 1
    return jsonify({"ok": True, "count": count_assessments(), "restored": restored, "skipped": skipped})


# Gunicorn / Render: initialize storage when the module loads
if USE_DB:
    try:
        ensure_db()
    except Exception as e:  # retried lazily on the first request (see pg())
        print("WARNING: Postgres init failed (will retry on first request):", e)
else:
    ensure_data()

if __name__ == "__main__":
    print("Using JSON file storage (set DATABASE_URL for permanent Postgres)" if not USE_DB else "Using Postgres storage")
    port = int(os.environ.get("PORT", 5000))
    print("=" * 50)
    print(" QRS Assessment Backend")
    print(f" Storage: {'Postgres' if USE_DB else 'JSON file'}")
    print(f" Open: http://localhost:{port}")
    print(f" Admin: http://localhost:{port}/admin.html")
    print(" Login: admin / qrs@2026")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
