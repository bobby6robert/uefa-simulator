from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# Oficjalne API Ekstraklasy
API_URL = "https://api.ekstraklasa.org/tables"

@app.route("/")
def home():
    return "UEFA Simulator działa 🚀"

@app.route("/polska")
def polska():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()  # wyrzuci błąd, jeśli status != 200
        data = r.json()
    except Exception as e:
        return jsonify({"error": "Nie udało się pobrać danych z Ekstraklasy", "details": str(e)}), 500

    table_data = []
    # Iterujemy po drużynach w tabeli
    for team in data["leagueTable"]["teams"]:
        table_data.append({
            "position": team.get("position"),
            "team": team.get("teamName"),
            "points": team.get("points")
        })

    return jsonify({
        "league": "Ekstraklasa",
        "table": table_data
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
