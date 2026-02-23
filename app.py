from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

EKSTRAKLASA_URL = "https://www.ekstraklasa.org/tabela"

@app.route("/")
def home():
    return "UEFA Simulator działa 🚀"

@app.route("/polska")
def polska():
    r = requests.get(EKSTRAKLASA_URL)
    soup = BeautifulSoup(r.text, "html.parser")

    table_data = []

    rows = soup.select("tr.table__row")
    for row in rows:
        pos = row.select_one("td.table__cell--position")
        team = row.select_one("td.table__cell--team")
        pts = row.select_one("td.table__cell--points")
        if pos and team and pts:
            table_data.append({
                "position": int(pos.text.strip()),
                "team": team.text.strip(),
                "points": int(pts.text.strip())
            })

    return jsonify({
        "league": "Ekstraklasa",
        "table": table_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
