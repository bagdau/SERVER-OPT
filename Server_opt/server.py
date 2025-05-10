from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from modules.database import DocumentDatabase
from modules.auth import AuthManager  # Если используешь модуль авторизации
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

db = DocumentDatabase(os.path.join(BASE_DIR, "secure_storage.db"))
auth = AuthManager(secret_key="SuperSecretKey123", db_path=os.path.join(BASE_DIR, "secure_storage.db"))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Веб-страницы ----------
@app.route("/")
def index():
    return redirect(url_for("auth_page"))

@app.route("/auth")
def auth_page():
    return render_template("auth.html")

@app.route("/2fa")
def two_factor_page():
    return render_template("2fa.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

# ---------- API ----------
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Имя пользователя и пароль обязательны!"}), 400

    if db.user_exists(username):
        return jsonify({"error": "Пользователь уже существует!"}), 409

    db.add_user(username, password)
    return jsonify({"message": "Регистрация успешно завершена!"})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not db.verify_user(username, password):
        return jsonify({"error": "Неверные учетные данные"}), 401

    # Пример возврата тестового токена
    return jsonify({"access_token": "dummy_token", "refresh_token": "dummy_refresh"})

@app.route("/api/verify-2fa", methods=["POST"])
def verify_2fa():
    data = request.get_json()
    code = data.get("code")

    # Тестовый код 2FA — 123456
    if code == "123456":
        return jsonify({"success": True})
    return jsonify({"success": False}), 400

@app.route("/api/upload", methods=["POST"])
def upload_document():
    file = request.files.get("file")
    category = request.form.get("category", "Uncategorized")
    tags = request.form.get("tags", "")

    if not file:
        return jsonify({"error": "Файл не предоставлен"}), 400

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    db.add_document(file.filename, file_path, category, tags)
    return jsonify({"message": "Файл успешно загружен и зашифрован!"})

@app.route("/api/download/<int:doc_id>", methods=["GET"])
def download_document(doc_id):
    output_path = os.path.join(UPLOAD_DIR, f"decrypted_{doc_id}.bin")
    db.decrypt_document(doc_id, output_path)

    return send_file(output_path, as_attachment=True)

@app.route("/api/search", methods=["GET"])
def search_documents():
    keyword = request.args.get("keyword", "")
    results = db.search_documents(keyword)
    return jsonify({"results": results})

@app.route("/favicon.ico")
def favicon():
    return send_file(os.path.join(BASE_DIR, "static", "favicon.ico"))

# ---------- Запуск ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
