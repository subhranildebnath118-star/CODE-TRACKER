from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__, static_folder="static")
CORS(app)

# =========================
# DATABASE
# =========================
def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            language TEXT,
            topic TEXT,
            UNIQUE(user_id, language, topic)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS streak (
            user_id INTEGER PRIMARY KEY,
            last_date TEXT,
            count INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# SERVE FRONTEND
# =========================
@app.route("/")
def home():
    return send_from_directory("static", "ui.html")

@app.route("/login-page")
def login_page():
    return send_from_directory("static", "login.html")

# =========================
# AUTH
# =========================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required"}), 400

    if len(password) < 4:
        return jsonify({"status": "error", "message": "Password too short"}), 400

    hashed = generate_password_hash(password)

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return jsonify({"status": "success", "message": "Account created"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Username already exists"}), 409
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cur.fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return jsonify({
            "status": "success",
            "user_id": user["id"],
            "username": username
        })

    return jsonify({"status": "error", "message": "Invalid username or password"}), 401

# =========================
# PROGRESS
# =========================
@app.route("/save-progress", methods=["POST"])
def save_progress():
    data = request.json or {}
    user_id = data.get("user_id")
    language = data.get("language")
    topics = data.get("topics", [])

    if not user_id or not language:
        return jsonify({"status": "error", "message": "Missing data"}), 400

    try:
        user_id = int(user_id)
    except:
        return jsonify({"status": "error", "message": "Invalid user_id"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        # Clear old progress for this language
        cur.execute("DELETE FROM progress WHERE user_id = ? AND language = ?", (user_id, language))

        # Insert new progress
        for topic in topics:
            cur.execute(
                "INSERT OR IGNORE INTO progress (user_id, language, topic) VALUES (?, ?, ?)",
                (user_id, language, topic)
            )

        # Update streak
        update_streak(cur, user_id)

        conn.commit()
        return jsonify({"status": "saved"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

@app.route("/get-progress", methods=["POST"])
def get_progress():
    data = request.json or {}
    user_id = data.get("user_id")
    language = data.get("language")

    try:
        user_id = int(user_id)
    except:
        return jsonify({"topics": []})

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT topic FROM progress WHERE user_id = ? AND language = ?",
        (user_id, language)
    )
    rows = cur.fetchall()
    conn.close()

    return jsonify({"topics": [row["topic"] for row in rows]})

# =========================
# STREAK
# =========================
def update_streak(cur, user_id):
    today = datetime.now().date()
    cur.execute("SELECT last_date, count FROM streak WHERE user_id = ?", (user_id,))
    row = cur.fetchone()

    if not row:
        cur.execute(
            "INSERT INTO streak (user_id, last_date, count) VALUES (?, ?, ?)",
            (user_id, str(today), 1)
        )
        return

    last_date = datetime.strptime(row["last_date"], "%Y-%m-%d").date()
    count = row["count"]

    if last_date == today:
        return
    elif last_date == today - timedelta(days=1):
        count += 1
    else:
        count = 1

    cur.execute(
        "UPDATE streak SET last_date = ?, count = ? WHERE user_id = ?",
        (str(today), count, user_id)
    )

@app.route("/get-streak", methods=["POST"])
def get_streak():
    data = request.json or {}
    user_id = data.get("user_id")

    try:
        user_id = int(user_id)
    except:
        return jsonify({"streak": 0})

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT count FROM streak WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()

    return jsonify({"streak": row["count"] if row else 0})

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)