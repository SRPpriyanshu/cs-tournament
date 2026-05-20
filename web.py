from flask import Flask, render_template, request, redirect, session, url_for
import json
import os

app = Flask(__name__)
app.secret_key = "secret123"  # change later

DATA_FILE = "data.json"

# 🔐 LOGIN DETAILS
USERNAME = "admin"
PASSWORD = "1234"


def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except:
        return {"teams": {}}


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    data = load()
    teams = data["teams"]

    sorted_teams = sorted(
        teams.items(),
        key=lambda x: x[1]["P"],
        reverse=True
    )

    return render_template("index.html", teams=sorted_teams)


# 🔐 LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")

        if user == USERNAME and pwd == PASSWORD:
            session["user"] = user
            return redirect("/admin")

        return "Invalid credentials ❌"

    return render_template("login.html")


# 🔐 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# 🔐 PROTECTED ADMIN
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "user" not in session:
        return redirect("/login")

    data = load()

    if request.method == "POST":
        team = request.form.get("team")

        if team:
            data["teams"][team] = {"M": 0, "W": 0, "L": 0, "D": 0, "P": 0}
            save(data)

        return redirect("/admin")

    return render_template("admin.html", teams=data["teams"])


@app.route("/delete/<team>")
def delete(team):
    if "user" not in session:
        return redirect("/login")

    data = load()
    data["teams"].pop(team, None)
    save(data)
    return redirect("/admin")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
