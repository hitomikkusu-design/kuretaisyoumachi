from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

DEFAULT_DATA = {
    "shops": ["山八", "コクや", "ポルタ", "プサカ"],
    "open_shops": []
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    data = load_data()
    return render_template(
        "index.html",
        shops=data["shops"],
        open_shops=data["open_shops"]
    )

@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load_data()
    saved = False

    if request.method == "POST":
        data["open_shops"] = request.form.getlist("open_shops")
        save_data(data)
        saved = True

    return render_template(
        "admin.html",
        shops=data["shops"],
        open_shops=data["open_shops"],
        saved=saved
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
