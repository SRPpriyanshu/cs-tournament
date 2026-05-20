from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


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


@app.route("/admin", methods=["GET", "POST"])
def admin():
    data = load()

    if request.method == "POST":
        team = request.form.get("team")

        if team:
            data["teams"][team] = {"M": 0, "W": 0, "L": 0, "D": 0, "P": 0}
            save(data)

        return redirect("/admin")

    return render_template("admin.html", teams=data["teams"])


@app.route("/edit/<team>", methods=["GET", "POST"])
def edit(team):
    data = load()

    if team not in data["teams"]:
        return "Team not found"

    if request.method == "POST":
        M = int(request.form.get("M") or 0)
        W = int(request.form.get("W") or 0)
        D = int(request.form.get("D") or 0)
        L = int(request.form.get("L") or 0)

        P = W * 3 + D

        data["teams"][team] = {
            "M": M,
            "W": W,
            "L": L,
            "D": D,
            "P": P
        }

        save(data)
        return redirect(f"/admin?updated={team}")

    return render_template("edit.html", team=team, data=data["teams"][team])


@app.route("/delete/<team>")
def delete(team):
    data = load()
    data["teams"].pop(team, None)
    save(data)
    return redirect("/admin")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)