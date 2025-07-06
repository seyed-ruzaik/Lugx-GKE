from flask import Flask, request, jsonify, Response
from supabase import create_client, Client
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

# Read Supabase credentials from environment variables
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Validate environment variables
if not url or not key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY not set")

# Initialize Supabase client
supabase: Client = create_client(url, key)

# Initialize Flask app
app = Flask(__name__)

# Prometheus metrics
order_counter = Counter('order_requests_total', 'Total number of /place-order POST requests')
fetch_counter = Counter('get_orders_total', 'Total number of /orders GET requests')

# API route to place a new order
@app.route("/place-order", methods=["POST"])
def place_order():
    order_counter.inc()
    try:
        data = request.json
        response = supabase.table("orders").insert({
            "customer": data["customer"],
            "items": str(data["items"]),
            "total": data["total"],
            "order_date": datetime.datetime.now().isoformat()
        }).execute()
        return jsonify({"message": "Order placed", "response": response.data}), 201
    except Exception as e:
        print("Supabase error:", e)
        return jsonify({"error": str(e)}), 500

# API route to fetch all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    fetch_counter.inc()
    try:
        response = supabase.table("orders").select("*").execute()
        return jsonify(response.data)
    except Exception as e:
        print("Supabase error:", e)
        return jsonify({"error": str(e)}), 500

# Prometheus /metrics endpoint
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
