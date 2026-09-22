#!/usr/bin/env python3
"""
QRS Assessment Platform - Backend
Supports:
  - Postgres (Supabase / Neon) via DATABASE_URL  → permanent storage
  - Local JSON files as fallback (dev / no DB)

Local:  python backend.py  → http://localhost:5000
Render: set DATABASE_URL env var to your Supabase/Neon connection string
"""
import json
import os
import secrets
import time
import uuid
from datetime import datetime
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

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

app = Flask(__name__, static_folder=BASE, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_pg():
    """Get a pooled connection using DATABASE_URL. Caller MUST return it with put_pg(conn)."""
    import psycopg2
    if not DATABASE_URL or "://" not in DATABASE_URL:
        raise RuntimeError("DATABASE_URL missing or invalid")
    global _pg_pool
    if _pg_pool is None:
        try:
            import psycopg2.pool
            # Small pool: Render free tier + Supabase/Neon free tiers both cap connections low.
            _pg_pool = psycopg2.pool.ThreadedConnectionPool(1, 8, DATABASE_URL, connect_timeout=20)
        except Exception as e:
            safe = DATABASE_URL
            if "@" in safe and "://" in safe:
                try:
                    pre, post = safe.split("@", 1)
                    if ":" in pre.split("://", 1)[-1]:
                        scheme_user, _pass = pre.rsplit(":", 1)
                        safe = scheme_user + ":***@" + post
                except Exception:
                    safe = "postgresql://***"
            print("Postgres pool init failed. Using URL like:", safe)
            raise e
    conn = _pg_pool.getconn()
    conn.autocommit = True
    return conn


def put_pg(conn):
    """Return a connection to the pool (or close it if there is no pool)."""
    global _pg_pool
    if _pg_pool is not None:
        try:
            _pg_pool.putconn(conn)
            return
        except Exception:
            pass
    try:
        conn.close()
    except Exception:
        pass


def db_init():
    if not USE_DB:
        return
    conn = get_pg()
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
    # Seed admin users if empty
    cur.execute("SELECT COUNT(*) FROM admin_users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO admin_users (username, password, role) VALUES (%s,%s,%s), (%s,%s,%s)",
            ("admin", "qrs@2026", "admin", "coordinator", "qrs@coord", "coordinator"),
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
                        """
                        INSERT INTO assessments (id, payload, status, name, email, updated_at)
                        VALUES (%s, %s::jsonb, %s, %s, %s, NOW())
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (
                            aid,
                            json.dumps(a),
                            a.get("status"),
                            a.get("name"),
                            a.get("email"),
                        ),
                    )
                print(f"Migrated {len(items)} assessments from JSON → Postgres")
        except Exception as e:
            print("JSON→DB migrate skipped:", e)
    cur.close()
    put_pg(conn)
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
                        {"user": "admin", "pass": "qrs@2026", "role": "admin"},
                        {"user": "coordinator", "pass": "qrs@coord", "role": "coordinator"},
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


def backup_assessments_file(data):
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
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT payload FROM assessments ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        put_pg(conn)
        out = []
        for (payload,) in rows:
            if isinstance(payload, str):
                payload = json.loads(payload)
            out.append(payload)
        return out
    ensure_data()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_assessments(data):
    """Replace full list (used by bulk ops). Prefer upsert_assessment for single updates."""
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        # Snapshot lightweight backup (strip huge media for backup size)
        slim = []
        for a in data:
            s = dict(a)
            if s.get("photoHistory") and len(s["photoHistory"]) > 2:
                s["photoHistory"] = s["photoHistory"][-2:]
            if s.get("videoHistory") and len(s["videoHistory"]) > 1:
                s["videoHistory"] = s["videoHistory"][-1:]
            slim.append(s)
        try:
            cur.execute(
                "INSERT INTO meta_backups (snapshot, note) VALUES (%s::jsonb, %s)",
                (json.dumps(slim), "auto-save"),
            )
            cur.execute(
                "DELETE FROM meta_backups WHERE id NOT IN (SELECT id FROM meta_backups ORDER BY created_at DESC LIMIT 20)"
            )
        except Exception as e:
            print("meta backup:", e)
        # Upsert all
        for a in data:
            aid = a.get("id")
            if not aid:
                continue
            cur.execute(
                """
                INSERT INTO assessments (id, payload, status, name, email, updated_at, created_at)
                VALUES (%s, %s::jsonb, %s, %s, %s, NOW(), COALESCE(
                    (SELECT created_at FROM assessments WHERE id=%s), NOW()
                ))
                ON CONFLICT (id) DO UPDATE SET
                    payload = EXCLUDED.payload,
                    status = EXCLUDED.status,
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    updated_at = NOW()
                """,
                (aid, json.dumps(a), a.get("status"), a.get("name"), a.get("email"), aid),
            )
        # Remove ids not in list
        ids = [a.get("id") for a in data if a.get("id")]
        if ids:
            cur.execute("DELETE FROM assessments WHERE id <> ALL(%s)", (ids,))
        else:
            cur.execute("DELETE FROM assessments")
        cur.close()
        put_pg(conn)
        return
    ensure_data()
    backup_assessments_file(data)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_one_assessment(aid):
    """Fetch a single candidate record without loading every other candidate's payload
    (which, with embedded photos/videos, made every single-candidate lookup very expensive)."""
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT payload FROM assessments WHERE id=%s", (aid,))
        row = cur.fetchone()
        cur.close()
        put_pg(conn)
        if not row:
            return None
        payload = row[0]
        if isinstance(payload, str):
            payload = json.loads(payload)
        return payload
    for a in load_assessments():
        if a.get("id") == aid:
            return a
    return None


def count_assessments():
    """Lightweight count for /api/health — avoids pulling every payload just to len() them."""
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM assessments")
        n = cur.fetchone()[0]
        cur.close()
        put_pg(conn)
        return n
    return len(load_assessments())


def delete_one_assessment(aid):
    """Delete a single candidate without rewriting the whole table."""
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("DELETE FROM assessments WHERE id=%s", (aid,))
        deleted = cur.rowcount > 0
        cur.close()
        put_pg(conn)
        return deleted
    data = load_assessments()
    new_data = [a for a in data if a.get("id") != aid]
    if len(new_data) == len(data):
        return False
    save_assessments(new_data)
    return True


def upsert_assessment(aid, body, merge_existing=True):
    """Insert or update ONE assessment. In DB mode this touches only that one row —
    it used to reload and rewrite the entire assessments table (including every other
    candidate's embedded photos/videos) on every single answer-sync or photo capture,
    which got slow and caused timeouts/dropped captures once there were several candidates."""
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT payload FROM assessments WHERE id=%s", (aid,))
        row = cur.fetchone()
        if row:
            existing = row[0]
            if isinstance(existing, str):
                existing = json.loads(existing)
            if merge_existing:
                merged = dict(existing)
                for k, v in body.items():
                    if k == "photoHistory" and not v and existing.get("photoHistory"):
                        continue
                    if k == "videoHistory" and not v and existing.get("videoHistory"):
                        continue
                    # Never wipe a saved numeric score with null/empty from a partial sync
                    if k == "score" and (v is None or v == "") and existing.get("score") is not None:
                        continue
                    if k == "answers" and (not v) and existing.get("answers"):
                        continue
                    if k == "completedAt" and not v and existing.get("completedAt"):
                        continue
                    merged[k] = v
                # Never let a late/stale sync downgrade a finished test back to in-progress/pending
                if body.get("status") == "completed":
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
                    if existing.get("answers") and not merged.get("answers"):
                        merged["answers"] = existing.get("answers")
            else:
                merged = dict(body)
                merged["id"] = aid
            cur.execute(
                "UPDATE assessments SET payload=%s::jsonb, status=%s, name=%s, email=%s, updated_at=NOW() WHERE id=%s",
                (json.dumps(merged), merged.get("status"), merged.get("name"), merged.get("email"), aid),
            )
            cur.close()
            put_pg(conn)
            return merged
        item = dict(body)
        item["id"] = aid
        cur.execute(
            "INSERT INTO assessments (id, payload, status, name, email) VALUES (%s,%s::jsonb,%s,%s,%s) "
            "ON CONFLICT (id) DO UPDATE SET payload=EXCLUDED.payload, status=EXCLUDED.status, "
            "name=EXCLUDED.name, email=EXCLUDED.email, updated_at=NOW()",
            (aid, json.dumps(item), item.get("status"), item.get("name"), item.get("email")),
        )
        cur.close()
        put_pg(conn)
        return item
    # File mode: fine to load/rewrite the whole (local disk, no network round trip)
    data = load_assessments()
    found = None
    for i, a in enumerate(data):
        if a.get("id") == aid:
            found = a
            if merge_existing:
                merged = dict(a)
                for k, v in body.items():
                    if k == "photoHistory" and not v and a.get("photoHistory"):
                        continue
                    if k == "videoHistory" and not v and a.get("videoHistory"):
                        continue
                    if k == "score" and (v is None or v == "") and a.get("score") is not None:
                        continue
                    if k == "answers" and (not v) and a.get("answers"):
                        continue
                    if k == "completedAt" and not v and a.get("completedAt"):
                        continue
                    merged[k] = v
                if body.get("status") == "completed":
                    merged["status"] = "completed"
                    if body.get("score") is not None:
                        merged["score"] = body.get("score")
                    if body.get("completedAt"):
                        merged["completedAt"] = body.get("completedAt")
                if a.get("status") == "completed":
                    if merged.get("status") in ("pending", "in-progress", "expired", "missed"):
                        merged["status"] = "completed"
                    if a.get("score") is not None and merged.get("score") is None:
                        merged["score"] = a.get("score")
                    if a.get("completedAt") and not merged.get("completedAt"):
                        merged["completedAt"] = a.get("completedAt")
                    if a.get("answers") and not merged.get("answers"):
                        merged["answers"] = a.get("answers")
                data[i] = merged
                found = merged
            else:
                data[i] = body
                found = body
            break
    if found is None:
        item = dict(body)
        item["id"] = aid
        data.append(item)
        found = item
    save_assessments(data)
    return found


def load_admin():
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT username, password, role FROM admin_users")
        rows = cur.fetchall()
        cur.close()
        put_pg(conn)
        return {"users": [{"user": r[0], "pass": r[1], "role": r[2]} for r in rows]}
    ensure_data()
    with open(ADMIN_FILE, "r") as f:
        return json.load(f)


def save_admin(cred):
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("DELETE FROM admin_users")
        for u in cred.get("users", []):
            cur.execute(
                "INSERT INTO admin_users (username, password, role) VALUES (%s,%s,%s)",
                (u.get("user"), u.get("pass"), u.get("role", "coordinator")),
            )
        cur.close()
        put_pg(conn)
        return
    with open(ADMIN_FILE, "w") as f:
        json.dump(cred, f, indent=2)


# ---------- Settings (currently: question bank overrides) ----------
# A small generic key/value JSON store, reusing the same DB-or-file pattern as
# admin credentials above. Used by the in-admin Question Bank editor so admins
# can add/edit questions without touching questions.js directly. Overrides are
# public to GET (candidates' test.html needs to read them too), but only an
# admin can write.
def load_settings():
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT value FROM settings WHERE key=%s", ("question_overrides",))
        row = cur.fetchone()
        cur.close()
        put_pg(conn)
        if row:
            v = row[0]
            return v if isinstance(v, dict) else json.loads(v)
        return {}
    if not os.path.exists(SETTINGS_FILE):
        return {}
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data):
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO settings (key, value, updated_at) VALUES (%s, %s::jsonb, NOW())
            ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW()
            """,
            ("question_overrides", json.dumps(data)),
        )
        cur.close()
        put_pg(conn)
        return
    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def append_media(aid, kind, data_url, meta=None):
    """Store photo/video. In DB mode uses assessment_media table + updates payload summary."""
    meta = meta or {}
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("SELECT payload FROM assessments WHERE id=%s", (aid,))
        row = cur.fetchone()
        if not row:
            cur.close()
            put_pg(conn)
            return None, "Not found"
        payload = row[0]
        if isinstance(payload, str):
            payload = json.loads(payload)
        cur.execute(
            "INSERT INTO assessment_media (assessment_id, kind, data, meta) VALUES (%s,%s,%s,%s::jsonb) RETURNING id",
            (aid, kind, data_url, json.dumps(meta)),
        )
        mid = cur.fetchone()[0]
        # Keep small preview on payload for admin UI
        at = meta.get("at") or datetime.utcnow().isoformat()
        if kind == "photo":
            hist = payload.get("photoHistory") or []
            hist.append({"img": data_url, "at": at, "mediaId": mid})
            # Cap embedded preview for payload size. At a 10s capture interval this
            # covers roughly 2.7 hours of a session — effectively the whole test for
            # any realistic duration. The FULL set of photos is always additionally
            # kept in assessment_media regardless of this cap.
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
            "UPDATE assessments SET payload=%s::jsonb, status=%s, updated_at=NOW() WHERE id=%s",
            (json.dumps(payload), payload.get("status"), aid),
        )
        cur.close()
        put_pg(conn)
        return payload, None
    # File mode
    data = load_assessments()
    for i, a in enumerate(data):
        if a.get("id") == aid:
            at = meta.get("at") or datetime.utcnow().isoformat()
            if kind == "photo":
                hist = a.get("photoHistory") or []
                hist.append({"img": data_url, "at": at})
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
    if USE_DB:
        conn = get_pg()
        cur = conn.cursor()
        cur.execute("DELETE FROM assessment_media WHERE assessment_id=%s", (aid,))
        cur.execute("SELECT payload FROM assessments WHERE id=%s", (aid,))
        row = cur.fetchone()
        if not row:
            cur.close()
            put_pg(conn)
            return False
        payload = row[0]
        if isinstance(payload, str):
            payload = json.loads(payload)
        payload["photoHistory"] = []
        payload["videoHistory"] = []
        payload["lastPhoto"] = None
        payload["lastPhotoAt"] = None
        payload["lastVideoAt"] = None
        cur.execute(
            "UPDATE assessments SET payload=%s::jsonb, updated_at=NOW() WHERE id=%s",
            (json.dumps(payload), aid),
        )
        cur.close()
        put_pg(conn)
        return True
    data = load_assessments()
    for i, a in enumerate(data):
        if a.get("id") == aid:
            a["photoHistory"] = []
            a["videoHistory"] = []
            a["lastPhoto"] = None
            a["lastPhotoAt"] = None
            a["lastVideoAt"] = None
            data[i] = a
            save_assessments(data)
            return True
    return False


# ---------- Auth ----------
ACTIVE_TOKENS = {}
TOKEN_TTL_SECONDS = 12 * 60 * 60


def issue_token(user, role):
    token = "qrs-" + secrets.token_hex(20)
    ACTIVE_TOKENS[token] = {"user": user, "role": role, "exp": time.time() + TOKEN_TTL_SECONDS}
    return token


def current_admin():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[len("Bearer ") :].strip()
    rec = ACTIVE_TOKENS.get(token)
    if not rec:
        return None
    if rec["exp"] < time.time():
        ACTIVE_TOKENS.pop(token, None)
        return None
    return rec


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
    return bool(supplied_token) and bool(record.get("token")) and supplied_token == record.get("token")


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

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20) as server:
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
    start_line = (
        f"The assessment will start on <strong>{unlock_at_str}</strong>."
        if unlock_at_str else
        "The assessment is available to start right away."
    )
    validity_hours_str = validity_hours or 24
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
    body = request.get_json(force=True) or {}
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"ok": False, "error": "Not found"}), 404
    to_email = body.get("email") or a.get("email")
    link = body.get("link")
    if not link:
        return jsonify({"ok": False, "error": "Missing link"}), 400
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


# ---------- Routes ----------
@app.route("/")
def index():
    return send_from_directory(BASE, "index.html")


@app.route("/admin.html")
def admin_page():
    return send_from_directory(BASE, "admin.html")


@app.route("/test.html")
def test_page():
    return send_from_directory(BASE, "test.html")


@app.route("/api/health")
def health():
    storage = "postgres" if USE_DB else "json-file"
    count = 0
    try:
        count = count_assessments()
    except Exception as e:
        return jsonify({"ok": False, "storage": storage, "error": str(e)}), 500
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


@app.route("/api/questions/<role>/<level>", methods=["PUT"])
def put_question_override(role, level):
    if not current_admin():
        return jsonify({"error": "Unauthorized"}), 401
    body = request.get_json(force=True) or {}
    questions = body.get("questions")
    if not isinstance(questions, list) or not questions:
        return jsonify({"error": "questions must be a non-empty list"}), 400
    for i, q in enumerate(questions):
        if not q.get("id") or not q.get("type") or not q.get("question"):
            return jsonify({"error": f"Question #{i+1} is missing id/type/question"}), 400
        if q.get("type") == "mcq" and (not q.get("options") or q.get("correct") is None):
            return jsonify({"error": f"Question #{i+1} (MCQ) needs options and a correct answer"}), 400
    duration = body.get("duration") or 45
    total_marks = sum(int(q.get("marks") or 0) for q in questions)
    overrides = load_settings()
    key = f"{role.lower()}/{level.lower()}"
    overrides[key] = {
        "duration": duration,
        "questions": questions,
        "totalMarks": total_marks,
        "updatedAt": datetime.utcnow().isoformat(),
        "updatedBy": (current_admin() or {}).get("user", "admin"),
    }
    save_settings(overrides)
    return jsonify({"ok": True, "totalMarks": total_marks})


@app.route("/api/questions/<role>/<level>", methods=["DELETE"])
def delete_question_override(role, level):
    """Revert a role/level back to the bundled questions.js defaults."""
    if not current_admin():
        return jsonify({"error": "Unauthorized"}), 401
    overrides = load_settings()
    key = f"{role.lower()}/{level.lower()}"
    if key in overrides:
        del overrides[key]
        save_settings(overrides)
    return jsonify({"ok": True})


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(force=True) or {}
    cred = load_admin()
    users = cred.get("users", [])
    match = next(
        (u for u in users if u.get("user") == body.get("user") and u.get("pass") == body.get("pass")),
        None,
    )
    if match:
        role = match.get("role", "coordinator")
        token = issue_token(match["user"], role)
        return jsonify({"ok": True, "token": token, "user": match["user"], "role": role})
    return jsonify({"ok": False, "error": "Invalid username or password"}), 401


@app.route("/api/admin/password", methods=["POST"])
@require_admin
def admin_password():
    body = request.get_json(force=True) or {}
    new_pass = body.get("pass") or ""
    if len(new_pass) < 6:
        return jsonify({"ok": False, "error": "Password min 6 chars"}), 400
    rec = current_admin()
    cred = load_admin()
    users = cred.get("users", [])
    for u in users:
        if u.get("user") == rec["user"]:
            u["pass"] = new_pass
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
    body = request.get_json(force=True) or {}
    username = (body.get("user") or "").strip()
    password = body.get("pass") or ""
    if not username or len(password) < 6:
        return jsonify({"ok": False, "error": "Username required, password min 6 chars"}), 400
    cred = load_admin()
    users = cred.get("users", [])
    if any(u.get("user") == username for u in users):
        return jsonify({"ok": False, "error": "That username already exists"}), 400
    users.append({"user": username, "pass": password, "role": "coordinator"})
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
    save_admin(cred)
    for tok, rec in list(ACTIVE_TOKENS.items()):
        if rec.get("user") == username:
            ACTIVE_TOKENS.pop(tok, None)
    return jsonify({"ok": True})


@app.route("/api/assessments", methods=["GET"])
@require_admin
def list_assessments():
    return jsonify(load_assessments())


@app.route("/api/assessments", methods=["POST"])
@require_admin
def create_assessment():
    body = request.get_json(force=True) or {}
    data = load_assessments()
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
    data.append(item)
    save_assessments(data)
    return jsonify(item), 201


@app.route("/api/assessments/<aid>", methods=["GET"])
def get_assessment(aid):
    a = get_one_assessment(aid)
    if not a:
        return jsonify({"error": "Not found"}), 404
    if current_admin() or candidate_token_ok(a, request.args.get("token")):
        return jsonify(a)
    return jsonify({"error": "Unauthorized"}), 401


@app.route("/api/assessments/<aid>", methods=["PUT"])
def update_assessment(aid):
    body = request.get_json(force=True) or {}
    admin_rec = current_admin()
    existing = get_one_assessment(aid)
    if existing:
        if not admin_rec and not candidate_token_ok(existing, body.get("token")):
            return jsonify({"ok": False, "error": "Unauthorized"}), 401
        # A candidate trying to start a test (pending -> in-progress) after the link has
        # expired is rejected here, even if their browser's own client-side check was
        # bypassed. Admins are exempt (e.g. reopening/editing an expired record).
        attempting_start = body.get("status") == "in-progress" and existing.get("status") == "pending"
        if not admin_rec and attempting_start and is_link_expired(existing):
            return jsonify({"ok": False, "error": "This link has expired."}), 403
        saved = upsert_assessment(aid, body, merge_existing=True)
        return jsonify(saved)
    if not admin_rec:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    item = upsert_assessment(aid, body, merge_existing=False)
    return jsonify(item), 201


@app.route("/api/assessments/<aid>/photos", methods=["POST"])
def add_photo(aid):
    body = request.get_json(force=True) or {}
    img = body.get("img")
    at = body.get("at") or datetime.utcnow().isoformat()
    if not img:
        return jsonify({"error": "img required"}), 400
    existing = get_one_assessment(aid)
    if not existing:
        return jsonify({"error": "Not found"}), 404
    admin_rec = current_admin()
    if not admin_rec and not candidate_token_ok(existing, body.get("token")):
        return jsonify({"error": "Unauthorized"}), 401
    payload, err = append_media(aid, "photo", img, {"at": at})
    if err:
        return jsonify({"error": err}), 404
    return jsonify({"ok": True, "count": len(payload.get("photoHistory") or [])})


@app.route("/api/assessments/<aid>/videos", methods=["POST"])
def add_video(aid):
    body = request.get_json(force=True) or {}
    video = body.get("video")
    at = body.get("at") or datetime.utcnow().isoformat()
    seconds = body.get("seconds") or 15
    if not video:
        return jsonify({"error": "video required"}), 400
    existing = get_one_assessment(aid)
    if not existing:
        return jsonify({"error": "Not found"}), 404
    admin_rec = current_admin()
    if not admin_rec and not candidate_token_ok(existing, body.get("token")):
        return jsonify({"error": "Unauthorized"}), 401
    payload, err = append_media(aid, "video", video, {"at": at, "seconds": seconds})
    if err:
        return jsonify({"error": err}), 404
    return jsonify({"ok": True, "count": len(payload.get("videoHistory") or [])})


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
    """Upload a list of assessments (from Backup JSON) into storage."""
    body = request.get_json(force=True) or {}
    items = body if isinstance(body, list) else body.get("assessments") or body.get("data") or []
    if not isinstance(items, list) or not items:
        return jsonify({"ok": False, "error": "Send a JSON array of assessments"}), 400
    data = load_assessments()
    by_id = {a.get("id"): a for a in data if a.get("id")}
    for a in items:
        aid = a.get("id")
        if not aid:
            continue
        if aid in by_id:
            # prefer completed
            old = by_id[aid]
            if a.get("status") == "completed" or old.get("status") != "completed":
                by_id[aid] = a
        else:
            by_id[aid] = a
    save_assessments(list(by_id.values()))
    return jsonify({"ok": True, "count": len(by_id)})


# Gunicorn / Render: initialize storage when the module loads
if USE_DB:
    try:
        db_init()
    except Exception as e:
        print("WARNING: Postgres init failed:", e)
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
