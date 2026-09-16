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
BACKUP_DIR = os.path.join(BASE, "data", "backups")
MAX_BACKUPS = 30

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
# Render sometimes uses postgres:// — psycopg2 wants postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = "postgresql://" + DATABASE_URL[len("postgres://"):]

USE_DB = bool(DATABASE_URL)
_pg = None

app = Flask(__name__, static_folder=BASE, static_url_path="")
CORS(app, resources={r"/api/*": {"origins": "*"}})


def get_pg():
    """Lazy import + connect. Returns connection (caller should close or use with)."""
    global _pg
    import psycopg2
    from psycopg2.extras import RealDictCursor
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=15)
    conn.autocommit = True
    return conn


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
    conn.close()
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
        conn.close()
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
        conn.close()
        return
    ensure_data()
    backup_assessments_file(data)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def upsert_assessment(aid, body, merge_existing=True):
    """Insert or update one assessment. Returns the saved record."""
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
                    merged[k] = v
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
        conn.close()
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
        conn.close()
        return
    with open(ADMIN_FILE, "w") as f:
        json.dump(cred, f, indent=2)


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
            conn.close()
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
            # Cap embedded history to last 30 for payload size; full set in media table
            if len(hist) > 30:
                hist = hist[-30:]
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
        conn.close()
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
            conn.close()
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
        conn.close()
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
        count = len(load_assessments())
    except Exception as e:
        return jsonify({"ok": False, "storage": storage, "error": str(e)}), 500
    return jsonify(
        {
            "ok": True,
            "backend": "flask",
            "storage": storage,
            "candidates": count,
            "time": datetime.utcnow().isoformat(),
        }
    )


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
    }
    data.append(item)
    save_assessments(data)
    return jsonify(item), 201


@app.route("/api/assessments/<aid>", methods=["GET"])
def get_assessment(aid):
    data = load_assessments()
    for a in data:
        if a.get("id") == aid:
            if current_admin() or candidate_token_ok(a, request.args.get("token")):
                return jsonify(a)
            return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"error": "Not found"}), 404


@app.route("/api/assessments/<aid>", methods=["PUT"])
def update_assessment(aid):
    body = request.get_json(force=True) or {}
    data = load_assessments()
    admin_rec = current_admin()
    for a in data:
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"ok": False, "error": "Unauthorized"}), 401
            saved = upsert_assessment(aid, body, merge_existing=True)
            return jsonify(saved)
    if not admin_rec:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    item = dict(body)
    item["id"] = aid
    data.append(item)
    save_assessments(data)
    return jsonify(item), 201


@app.route("/api/assessments/<aid>/photos", methods=["POST"])
def add_photo(aid):
    body = request.get_json(force=True) or {}
    img = body.get("img")
    at = body.get("at") or datetime.utcnow().isoformat()
    if not img:
        return jsonify({"error": "img required"}), 400
    data = load_assessments()
    admin_rec = current_admin()
    for a in data:
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"error": "Unauthorized"}), 401
            _, err = append_media(aid, "photo", img, {"at": at})
            if err:
                return jsonify({"error": err}), 404
            a2 = next(x for x in load_assessments() if x.get("id") == aid)
            return jsonify({"ok": True, "count": len(a2.get("photoHistory") or [])})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/assessments/<aid>/videos", methods=["POST"])
def add_video(aid):
    body = request.get_json(force=True) or {}
    video = body.get("video")
    at = body.get("at") or datetime.utcnow().isoformat()
    seconds = body.get("seconds") or 15
    if not video:
        return jsonify({"error": "video required"}), 400
    data = load_assessments()
    admin_rec = current_admin()
    for a in data:
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"error": "Unauthorized"}), 401
            _, err = append_media(aid, "video", video, {"at": at, "seconds": seconds})
            if err:
                return jsonify({"error": err}), 404
            a2 = next(x for x in load_assessments() if x.get("id") == aid)
            return jsonify({"ok": True, "count": len(a2.get("videoHistory") or [])})
    return jsonify({"error": "Not found"}), 404


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
    data = load_assessments()
    new_data = [a for a in data if a.get("id") != aid]
    if len(new_data) == len(data):
        return jsonify({"error": "Not found"}), 404
    save_assessments(new_data)
    return jsonify({"ok": True, "deleted": aid})


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
    app.run(host="0.0.0.0", port=port, debug=False)
