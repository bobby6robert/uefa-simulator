from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "UEFA Simulator działa 🚀"

@app.route("/polska")
def polska():
    data = {
        "league": "Ekstraklasa",
        "table": [
            {"position": 1, "team": "Test FC", "points": 60},
            {"position": 2, "team": "Demo United", "points": 55}
        ]
    }
    return jsonify(data)
