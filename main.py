
from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

ADMIN_USERNAME = "zerow21admin"
ADMIN_PASSWORD = "zerow21adminpanel"
VALID_USERNAME = "usernfs"
VALID_PASSWORD = "usernfs"
LOG_FILE = "users.json"

def save_login(username, device):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"username": username, "device": device, "time": now}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    return "<h2>Zerow 21 Sunucu Aktif!</h2>"

@app.route("/login-acc", methods=["POST"])
def login_acc():
    username = request.form.get("username")
    password = request.form.get("password")
    device = request.form.get("device", "Unknown")
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        save_login(username, device)
        return jsonify({"status": True, "message": "Giriş başarılı"})
    return jsonify({"status": False, "message": "Hatalı kullanıcı adı veya şifre"})

@app.route("/termux-version")
def termux_version():
    return jsonify({
        "version": "2.6.10",
        "download_url": "https://raw.githubusercontent.com/zerow21/zerow21-cpm/main/zerow21_script.py"
    })

@app.route("/admin-panel", methods=["GET", "POST"])
def admin_panel():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, "r") as f:
                    logs = json.load(f)
            else:
                logs = []
            html = "<h2>Giriş Kayıtları</h2><table border=1><tr><th>Kullanıcı</th><th>Cihaz</th><th>Tarih</th></tr>"
            for log in logs:
                html += f"<tr><td>{log['username']}</td><td>{log['device']}</td><td>{log['time']}</td></tr>"
            html += "</table><br><a href='/admin-panel'>Geri dön</a>"
            return html
        return "<p>Hatalı giriş</p><a href='/admin-panel'>Tekrar dene</a>"
    return """<form method='POST'>
  <h2>Admin Panel Girişi</h2>
  Kullanıcı Adı: <input name='username'><br>
  Şifre: <input type='password' name='password'><br>
  <button type='submit'>Giriş Yap</button>
</form>"""

@app.route("/get_menu")
def get_menu():
    return jsonify({"options": ["CPM1 Feature A", "CPM1 Feature B"]})

@app.route("/get_menu_cpm2")
def get_menu_cpm2():
    return jsonify({"options": ["CPM2 Feature A", "CPM2 Feature B"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
