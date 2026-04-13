"""
LoL Draft Simulator — Flask Backend
====================================
Run:
    pip install flask
    python app.py

Then open: http://localhost:5000

API endpoint for ML recommendations:
    POST /api/recommend
    Body: { "step": int, "draft": { blue: {...}, red: {...} } }
    Returns: { "recommendations": [{ "name": str, "pct": int }] }
"""

from flask import Flask, jsonify, request, send_from_directory
import os
import random

app = Flask(__name__, static_folder=".")


# ──────────────────────────────────────────────
#  Serve the frontend
# ──────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "draft_simulator.html")


# ──────────────────────────────────────────────
#  Recommendation endpoint
#  Replace the mock logic below with your real ML models
# ──────────────────────────────────────────────
@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    step = data.get("step", 0)
    draft = data.get("draft", {})

    # Collect already used champions
    blue = draft.get("blue", {})
    red  = draft.get("red",  {})
    used = set(
        filter(None, blue.get("bans", []) + blue.get("picks", []) +
                      red.get("bans",  []) + red.get("picks",  []))
    )

    # ── Swap this block with your ML model ──────────────────────────────
    #
    # Example skeleton for your own model:
    #
    #   from your_model import DraftModel
    #   model = DraftModel.load("checkpoints/synergy_v2.pt")
    #
    #   recommendations = model.predict(
    #       step=step,
    #       blue_picks=blue.get("picks", []),
    #       blue_bans=blue.get("bans", []),
    #       red_picks=red.get("picks", []),
    #       red_bans=red.get("bans", []),
    #       top_k=3
    #   )
    #   # recommendations should be [{"name": str, "pct": float}]
    #
    # ────────────────────────────────────────────────────────────────────

    # Mock: random suggestions from the full champion pool
    CHAMPIONS = [
        "Ahri","Akali","Aatrox","Ambessa","Amumu","Annie","Aphelios","Ashe","Azir","Bard",
        "Blitzcrank","Brand","Braum","Caitlyn","Camille","Cassiopeia","Corki","Darius","Diana",
        "Draven","Ekko","Elise","Evelynn","Ezreal","Fiora","Fizz","Galio","Gangplank","Garen",
        "Graves","Hecarim","Irelia","Jayce","Jhin","Jinx","Kai'Sa","Kassadin","Katarina","Kayle",
        "Kennen","KogMaw","LeBlanc","LeeSin","Leona","Lissandra","Lucian","Lulu","Lux",
        "Malphite","Maokai","MasterYi","Morgana","Nami","Nautilus","Nidalee","Nilah","Nocturne",
        "Nunu","Olaf","Orianna","Pantheon","Poppy","Pyke","Qiyana","Rammus","RekSai","Renata",
        "Renekton","Riven","Rumble","Ryze","Sejuani","Senna","Seraphine","Sett","Shyvana",
        "Singed","Sion","Sivir","Skarner","Smolder","Syndra","Taliyah","Talon","Thresh",
        "TwistedFate","Twitch","Urgot","Varus","Vayne","Veigar","Vex","Viktor","Vladimir",
        "Volibear","Warwick","Xayah","Xerath","Yasuo","Zed","Zeri","Ziggs","Zilean","Zoe",
        "Zyra","Akshan","Aurora","Briar","Hwei","Yone"
    ]
    pool = [c for c in CHAMPIONS if c not in used]
    sample = random.sample(pool, min(3, len(pool)))

    w1 = random.randint(40, 60)
    w2 = random.randint(20, 35)
    w3 = max(5, 100 - w1 - w2)

    recommendations = [
        {"name": sample[0], "pct": w1},
        {"name": sample[1], "pct": w2},
        {"name": sample[2], "pct": w3},
    ] if len(sample) >= 3 else [{"name": c, "pct": 33} for c in sample]

    return jsonify({"recommendations": recommendations, "step": step})


if __name__ == "__main__":
    print("Draft simulator running at http://localhost:5000")
    app.run(debug=True, port=5000)
