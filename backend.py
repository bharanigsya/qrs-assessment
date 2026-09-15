#!/usr/bin/env python3
"""
QRS Assessment Platform - Backend
Local run:  python backend.py  ->  http://localhost:5000
Hosted (e.g. Render): reads PORT from the environment automatically.
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

app = Flask(__name__, static_folder=BASE, static_url_path="")
# Allow the API to be called from a separately-hosted frontend (e.g. Netlify).
# If you want to lock this down to just your Netlify domain, replace "*" with
# e.g. "https://your-site.netlify.app".
CORS(app, resources={r"/api/*": {"origins": "*"}})

def ensure_data():
    os.makedirs(os.path.join(BASE, "data"), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(ADMIN_FILE):
        with open(ADMIN_FILE, "w") as f:
            json.dump({
                "users": [
                    {"user": "admin", "pass": "qrs@2026", "role": "admin"},
                    {"user": "coordinator", "pass": "qrs@coord", "role": "coordinator"},
                ]
            }, f, indent=2)
    else:
        # Migrate the old single-user format {"user":..,"pass":..} to the multi-user format.
        with open(ADMIN_FILE, "r") as f:
            try:
                cred = json.load(f)
            except Exception:
                cred = {}
        if "users" not in cred:
            legacy_user = cred.get("user", "admin")
            legacy_pass = cred.get("pass", "qrs@2026")
            cred = {
                "users": [
                    {"user": legacy_user, "pass": legacy_pass, "role": "admin"},
                    {"user": "coordinator", "pass": "qrs@coord", "role": "coordinator"},
                ]
            }
            with open(ADMIN_FILE, "w") as f:
                json.dump(cred, f, indent=2)

def load_assessments():
    ensure_data()
    with open(DATA_FILE, "r") as f:
        return json.load(f)

BACKUP_DIR = os.path.join(BASE, "data", "backups")
MAX_BACKUPS = 30

def backup_assessments():
    """Copy the current assessments.json to a timestamped backup before it gets overwritten."""
    if not os.path.exists(DATA_FILE):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S-%f")
    backup_path = os.path.join(BACKUP_DIR, f"assessments-{ts}.json")
    try:
        with open(DATA_FILE, "r") as src, open(backup_path, "w") as dst:
            dst.write(src.read())
    except Exception as e:
        print("Backup failed:", e)
        return
    # Prune old backups, keep the most recent MAX_BACKUPS
    backups = sorted(
        (f for f in os.listdir(BACKUP_DIR) if f.startswith("assessments-")),
        reverse=True
    )
    for old in backups[MAX_BACKUPS:]:
        try:
            os.remove(os.path.join(BACKUP_DIR, old))
        except OSError:
            pass

def save_assessments(data):
    ensure_data()
    backup_assessments()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_admin():
    ensure_data()
    with open(ADMIN_FILE, "r") as f:
        return json.load(f)

def save_admin(cred):
    with open(ADMIN_FILE, "w") as f:
        json.dump(cred, f, indent=2)

# ========================================================================
# Auth — admin + coordinator accounts, session tokens actually checked
# server-side (not just a role flag trusted from the browser).
# ========================================================================
ACTIVE_TOKENS = {}  # token -> {"user": str, "role": "admin"|"coordinator", "exp": epoch_seconds}
TOKEN_TTL_SECONDS = 12 * 60 * 60  # 12 hours

def issue_token(user, role):
    token = "qrs-" + secrets.token_hex(20)
    ACTIVE_TOKENS[token] = {"user": user, "role": role, "exp": time.time() + TOKEN_TTL_SECONDS}
    return token

def current_admin():
    """Return {'user','role'} if this request carries a valid, unexpired admin/coordinator token."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[len("Bearer "):].strip()
    rec = ACTIVE_TOKENS.get(token)
    if not rec:
        return None
    if rec["exp"] < time.time():
        ACTIVE_TOKENS.pop(token, None)
        return None
    return rec

def require_admin(fn):
    """Any logged-in user (admin or coordinator)."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_admin():
            return jsonify({"ok": False, "error": "Unauthorized — please log in again"}), 401
        return fn(*args, **kwargs)
    return wrapper

def require_primary_admin(fn):
    """Only the primary admin role, e.g. for managing team accounts."""
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
    return jsonify({"ok": True, "backend": "flask", "time": datetime.utcnow().isoformat()})

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(force=True) or {}
    cred = load_admin()
    users = cred.get("users", [])
    match = next(
        (u for u in users if u.get("user") == body.get("user") and u.get("pass") == body.get("pass")),
        None
    )
    if match:
        role = match.get("role", "coordinator")
        token = issue_token(match["user"], role)
        return jsonify({"ok": True, "token": token, "user": match["user"], "role": role})
    return jsonify({"ok": False, "error": "Invalid username or password"}), 401

@app.route("/api/admin/password", methods=["POST"])
@require_admin
def admin_password():
    """Change the CURRENTLY LOGGED-IN user's own password."""
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

# ---- Team accounts ----
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

# ---- Assessments ----
@app.route("/api/assessments", methods=["GET"])
@require_admin
def list_assessments():
    """Full candidate list (names, emails, photos, videos...) — admin/coordinator only."""
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
    """A candidate can fetch their own record with ?token=... ; admin/coordinator can fetch any."""
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
    for i, a in enumerate(data):
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"ok": False, "error": "Unauthorized"}), 401
            # Don't wipe huge photo/video history if not sent
            merged = dict(a)
            for k, v in body.items():
                if k == "photoHistory" and not v and a.get("photoHistory"):
                    continue
                if k == "videoHistory" and not v and a.get("videoHistory"):
                    continue
                merged[k] = v
            data[i] = merged
            save_assessments(data)
            return jsonify(merged)
    # Not found locally yet — only an admin/coordinator can create a brand-new record this way.
    if not admin_rec:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    item = dict(body)
    item["id"] = aid
    data.append(item)
    save_assessments(data)
    return jsonify(item), 201

@app.route("/api/assessments/<aid>/photos", methods=["POST"])
def add_photo(aid):
    """Append one proctor photo without sending full history each time."""
    body = request.get_json(force=True) or {}
    img = body.get("img")
    at = body.get("at") or datetime.utcnow().isoformat()
    if not img:
        return jsonify({"error": "img required"}), 400
    data = load_assessments()
    admin_rec = current_admin()
    for i, a in enumerate(data):
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"error": "Unauthorized"}), 401
            hist = a.get("photoHistory") or []
            hist.append({"img": img, "at": at})
            a["photoHistory"] = hist
            a["lastPhoto"] = img
            a["lastPhotoAt"] = at
            data[i] = a
            save_assessments(data)
            return jsonify({"ok": True, "count": len(hist)})
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

@app.route("/api/assessments/<aid>/videos", methods=["POST"])
def add_video(aid):
    """Append one short proctor video clip."""
    body = request.get_json(force=True) or {}
    video = body.get("video")
    at = body.get("at") or datetime.utcnow().isoformat()
    seconds = body.get("seconds") or 30
    if not video:
        return jsonify({"error": "video required"}), 400
    data = load_assessments()
    admin_rec = current_admin()
    for i, a in enumerate(data):
        if a.get("id") == aid:
            if not admin_rec and not candidate_token_ok(a, body.get("token")):
                return jsonify({"error": "Unauthorized"}), 401
            hist = a.get("videoHistory") or []
            hist.append({"video": video, "at": at, "seconds": seconds})
            # Cap stored clips to control disk size on free hosts
            if len(hist) > 20:
                hist = hist[-20:]
            a["videoHistory"] = hist
            a["lastVideoAt"] = at
            data[i] = a
            save_assessments(data)
            return jsonify({"ok": True, "count": len(hist)})
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    ensure_data()
    port = int(os.environ.get("PORT", 5000))
    print("=" * 50)
    print(" QRS Assessment Backend")
    print(f" Open: http://localhost:{port}")
    print(f" Admin: http://localhost:{port}/admin.html")
    print(" Login: admin / qrs@2026")
    print("=" * 50)
    app.run(host="0.0.0.0", port=port, debug=False)
