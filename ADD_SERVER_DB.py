from flask import Flask, request, jsonify
import sqlite3
import hashlib
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secure_storage.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT
            );
        """)
        conn.commit()

init_db()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Имя пользователя и пароль обязательны!"}), 400

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                (username, password_hash)
            )
            conn.commit()
        return jsonify({"message": "Регистрация успешна!"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Пользователь уже существует!"}), 409

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM users WHERE username = ? AND password_hash = ?", 
            (username, password_hash)
        )
        if cursor.fetchone():
            return jsonify({"message": "Вход выполнен успешно!"})
        else:
            return jsonify({"error": "Неверные данные!"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
