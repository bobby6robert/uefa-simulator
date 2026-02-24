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

@app.route("/tabela/<country>")
def get_table(country):
    country = country.lower()
    if country not in LEAGUES:
        return jsonify({"error": f"Kraj '{country}' nie jest obsługiwany."}), 404

    suffix, l_type = LEAGUES[country]
    year = "2025-2026" if l_type == "j-w" else "2025"
    url = f"https://www.worldfootball.net/competition/{suffix}-{year}/"

    try:
        # Rozbudowane nagłówki, by udawać prawdziwą przeglądarkę
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.google.com/'
        }
        
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Próbujemy znaleźć jakąkolwiek tabelę, jeśli klasa standard_tabelle zawiedzie
        table = soup.find("table", class_="standard_tabelle")
        if not table:
            # Szukamy pierwszej tabeli, która ma wiersze (tr)
            all_tables = soup.find_all("table")
            for t in all_tables:
                if "Pos" in t.text or "Team" in t.text:
                    table = t
                    break

        if not table:
            return jsonify({
                "error": "Nie znaleziono tabeli",
                "debug_url": url,
                "html_preview": r.text[:500] # Pomoże nam zobaczyć, co serwer faktycznie dostał
            }), 500

        results = []
        rows = table.find_all("tr")
        
        for row in rows:
            cols = row.find_all("td")
            # Większość tabel ligowych ma od 8 do 11 kolumn
            if len(cols) >= 9:
                results.append({
                    "pos": cols[0].text.strip().replace(".", ""),
                    "team": cols[2].text.strip(),
                    "pts": cols[-1].text.strip() # Punkty są zazwyczaj w ostatniej kolumnie
                })
        
        return jsonify({
            "league": country.capitalize(),
            "url": url,
            "data": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
