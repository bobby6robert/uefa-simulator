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
    try:
        r = requests.get(EKSTRAKLASA_URL, timeout=10)
        r.raise_for_status()
    except Exception as e:
        return jsonify({"error": "Nie udało się pobrać strony Ekstraklasy", "details": str(e)}), 500

    soup = BeautifulSoup(r.text, "html.parser")
    table_data = []

    # Pobieramy drużyny z tabeli
    rows = soup.select("div.table__row")  # <div> zamiast <tr> – bo strona używa divów
    for row in rows:
        pos = row.select_one("div.table__cell--position")
        team = row.select_one("div.table__cell--team-name")  # poprawiona klasa
        pts = row.select_one("div.table__cell--points")
        if pos and team and pts:
            try:
                table_data.append({
                    "position": int(pos.text.strip()),
                    "team": team.text.strip(),
                    "points": int(pts.text.strip())
                })
            except:
                continue  # jeśli konwersja do int się nie uda

    return jsonify({
        "league": "Ekstraklasa",
        "table": table_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
