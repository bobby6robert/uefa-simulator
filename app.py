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
    rows = soup.select("table.league-table tbody tr")  # <- sprawdzić HTML
    for row in rows:
        position = row.select_one("td.position").text.strip()
        team = row.select_one("td.team").text.strip()
        points = row.select_one("td.points").text.strip()
        table_data.append({
            "position": int(position),
            "team": team,
            "points": int(points)
        })

    return jsonify({
        "league": "Ekstraklasa",
        "table": table_data
    })
