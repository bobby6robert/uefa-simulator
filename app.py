from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Słownik suffixów WorldFootball dla wszystkich 55 nacji (przykładowa lista - uzupełnij o resztę wg wzoru)
LEAGUES = {
    "england": ("eng-premier-league", "j-w"),
    "poland": ("pol-ekstraklasa", "j-w"),
    "germany": ("bundesliga", "j-w"),
    "italy": ("ita-serie-a", "j-w"),
    "france": ("fra-ligue-1", "j-w"),
    "norway": ("nor-eliteserien", "w-j"),
    "turkey": ("tur-sueper-lig", "j-w"),
    "denmark": ("den-superliga", "j-w")
}

@app.route("/")
def home():
    # Strona główna z listą klikalnych linków
    links = "".join([f'<li><a href="/tabela/{k}">{k.capitalize()}</a></li>' for k in LEAGUES.keys()])
    return f"<h1>UEFA Simulator API 🚀</h1><p>Wybierz ligę:</p><ul>{links}</ul>"

@app.route("/tabela/<country>")
def get_table(country):
    country = country.lower()
    if country not in LEAGUES:
        return jsonify({"error": f"Kraj '{country}' nie jest obsługiwany. Sprawdź listę na stronie głównej."}), 404

    suffix, l_type = LEAGUES[country]
    year = "2025-2026" if l_type == "j-w" else "2025"
    url = f"https://www.worldfootball.net/competition/{suffix}-{year}/"

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        table = soup.find("table", class_="standard_tabelle")
        if not table:
            return jsonify({"error": "Nie znaleziono tabeli na stronie źródłowej"}), 500

        results = []
        for row in table.find_all("tr")[1:]: # Pomijamy nagłówek
            cols = row.find_all("td")
            if len(cols) >= 10:
                results.append({
                    "pos": cols[0].text.strip().replace(".", ""),
                    "team": cols[2].text.strip(),
                    "pts": cols[9].text.strip()
                })
        
        return jsonify({
            "league": country.capitalize(),
            "season": year,
            "data": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
