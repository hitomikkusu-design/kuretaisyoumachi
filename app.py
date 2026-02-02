import os
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})



def get_shops():
    res = supabase.table("shops").select("*").order("id").execute()
    return res.data or []


def add_shop(name: str):
    supabase.table("shops").insert({"name": name, "is_open": False}).execute()


def set_open_shops(open_ids):
    # いったん全店を休みにしてから、チェックされた店だけ営業にする
    supabase.table("shops").update({"is_open": False}).neq("id", 0).execute()
    if open_ids:
        # open_ids は文字列で来るので int に
        open_ids_int = [int(x) for x in open_ids]
        supabase.table("shops").update({"is_open": True}).in_("id", open_ids_int).execute()


@app.route("/")
def home():
    shops = get_shops()
    open_shops = [s for s in shops if s.get("is_open")]
    return render_template("index.html", shops=shops, open_shops=open_shops)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    saved = False

    if request.method == "POST":
        # お店追加
        new_shop = request.form.get("new_shop", "").strip()
        if new_shop:
            add_shop(new_shop)

        # 今日の営業チェック
        open_ids = request.form.getlist("open_ids")
        set_open_shops(open_ids)

        saved = True

    shops = get_shops()
    return render_template("admin.html", shops=shops, saved=saved)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
