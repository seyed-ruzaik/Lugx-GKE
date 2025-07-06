from flask import Flask, request, jsonify, Response
from supabase import create_client, Client
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
import os

# Load environment variables from .env if available
load_dotenv()

# Read Supabase credentials from environment variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Check if credentials are set properly
if not url or not key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY environment variable not set")

# Create Supabase client instance
supabase: Client = create_client(url, key)

# Initialize Flask app
app = Flask(__name__)

# Prometheus metrics
game_add_counter = Counter('add_game_requests_total', 'Total number of /add-game POST requests')
game_fetch_counter = Counter('get_games_requests_total', 'Total number of /games GET requests')

# Route to add a new game
@app.route("/add-game", methods=["POST"])
def add_game():
    game_add_counter.inc()
    try:
        data = request.json
        response = supabase.table("games").insert({
            "name": data["name"],
            "category": data["category"],
            "release_date": data["release_date"],
            "price": data["price"]
        }).execute()
        return jsonify({"message": "Game added!", "response": response.data}), 201
    except Exception as e:
        print("Supabase error:", e)
        return jsonify({"error": str(e)}), 500

# Route to fetch all games
@app.route("/games", methods=["GET"])
def get_games():
    game_fetch_counter.inc()
    try:
        response = supabase.table("games").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        print("Supabase error:", e)
        return jsonify({"error": str(e)}), 500

# Prometheus metrics route
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
