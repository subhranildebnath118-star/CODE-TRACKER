from flask import Flask, request, jsonify, send_from_directory
import sqlite3
from flask_cors import CORS
from datetime import datetime, timedelta
import os

app = Flask(__name__, static_folder="static")
CORS(app)

# =========================
# DATABASE HELPER
# =========================
def connect_db():
    # check_same_thread=False is needed for SQLite in Flask
    return sqlite3.connect("database.db", check_same_thread=False)

def init_db():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS progress(user_id INTEGER, language TEXT, topic TEXT, completed INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS streak(user_id INTEGER, last_date TEXT, count INTEGER)")
    conn.commit()
    conn.close()

init_db()

# =========================
# SERVE PAGES
# =========================
@app.route("/")
def serve_ui():
    return send_from_directory("static", "ui.html")

@app.route("/login-page")
def login_page():
    return send_from_directory("static", "login.html")

# =========================
# AUTHENTICATION
# =========================
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (data["username"], data["password"]))
        conn.commit()
        return jsonify({"status": "success"})
    except:
        return jsonify({"status": "error", "message": "User already exists"})
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (data["username"], data["password"]))
    user = cur.fetchone()
    conn.close()
    if user:
        return jsonify({"status": "success", "user_id": user[0]})
    return jsonify({"status": "error"})

# =========================
# PROGRESS & STREAK
# =========================
@app.route("/save-progress", methods=["POST"])
def save_progress():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM progress WHERE user_id=? AND language=?", (data["user_id"], data["language"]))
    for topic in data["topics"]:
        cur.execute("INSERT INTO progress VALUES (?, ?, ?, 1)", (data["user_id"], data["language"], topic))
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})

@app.route("/get-progress", methods=["POST"])
def get_progress():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT topic FROM progress WHERE user_id=? AND language=?", (data["user_id"], data["language"]))
    rows = cur.fetchall()
    conn.close()
    return jsonify({"topics": [r[0] for r in rows]})

if __name__ == "__main__":
    app.run(debug=True)