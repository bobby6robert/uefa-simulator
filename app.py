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
    try:
        r = requests.get(EKSTRAKLASA_URL, timeout=10)
        r.raise_for_status()  # sprawdza, czy status 200 OK
    except requests.RequestException as e:
        return jsonify({"error": "Nie udało się pobrać danych", "details": str(e)}), 500

    soup = BeautifulSoup(r.text, "html.parser")
    table_data = []

    # Pobieramy wszystkie wiersze tabeli
    rows = soup.select("tr.table__row")
    for row in rows:
        pos = row.select_one("td.table__cell--position")
        team = row.select_one("td.table__cell--team")
        pts = row.select_one("td.table__cell--points")
        
        # Pomijamy wiersze bez danych
        if not pos or not team or not pts:
            continue

        try:
            table_data.append({
                "position": int(pos.get_text(strip=True)),
                "team": team.get_text(strip=True),
                "points": int(pts.get_text(strip=True))
            })
        except ValueError:
            # jeśli nie da się zamienić na int, pomijamy wiersz
            continue

    return jsonify({
        "league": "Ekstraklasa",
        "table": table_data
    })

if __name__ == "__main__":
    app.run(debug=True)
