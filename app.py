from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

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

    # To przykład, trzeba dopasować selektory do strony ekstraklasy
    rows = soup.select("tr.table__row")  # wszystkie wiersze tabeli
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
