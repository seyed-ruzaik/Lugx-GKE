# Import necessary libraries
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import clickhouse_connect
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
import os

# Load environment variables from .env if available
load_dotenv()

# Read ClickHouse credentials from environment variables
host = os.environ.get("CLICKHOUSE_HOST")
username = os.environ.get("CLICKHOUSE_USERNAME")
password = os.environ.get("CLICKHOUSE_PASSWORD")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Prometheus metrics
analytics_counter = Counter('track_requests_total', 'Total number of /track POST requests')

# Attempt to connect to ClickHouse and create table
try:
    if not host or not username or not password:
        raise ValueError("Missing ClickHouse environment variables")

    client = clickhouse_connect.get_client(
        host=host,
        username=username,
        password=password,
        secure=True
    )

    client.command('''
        CREATE TABLE IF NOT EXISTS web_analytics (
            id UUID DEFAULT generateUUIDv4(),
            event_type String,
            page_url String,
            user_agent String,
            timestamp DateTime DEFAULT now()
        ) ENGINE = MergeTree()
        ORDER BY (timestamp)
    ''')
except Exception as e:
    print("ClickHouse connection failed:", str(e))
    client = None

# API endpoint to track web analytics events
@app.route("/track", methods=["POST"])
def track_event():
    analytics_counter.inc()
    try:
        if client is None:
            return jsonify({"error": "ClickHouse client not available"}), 500

        data = request.json
        event_type = data.get("event_type")
        page_url = data.get("page_url")
        user_agent = request.headers.get("User-Agent", "Unknown")

        if not event_type or not page_url:
            return jsonify({"error": "Missing fields"}), 400

        client.insert(
            'web_analytics',
            [[event_type, page_url, user_agent]],
            column_names=['event_type', 'page_url', 'user_agent']
        )

        return jsonify({"message": "Event recorded"}), 201

    except Exception as e:
        print("Insert failed:", str(e))
        return jsonify({"error": str(e)}), 500

# Prometheus /metrics endpoint
@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
