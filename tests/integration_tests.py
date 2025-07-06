import requests

# ----------- Test Order Service -----------
def test_order_service_get():
    """
    Test GET request to /orders endpoint of order service.
    """
    try:
        res = requests.get("http://34.93.184.130:5001/orders")
        assert res.status_code == 200
        print("Order Service GET OK")
    except Exception as e:
        print("Order Service GET Failed:", e)

def test_order_service_post():
    """
    Test POST request to /place-order endpoint.
    """
    try:
        payload = {
            "customer": "Ruzaik",
            "items": ["Call of Duty 2", "FIFA 25"],
            "total": 120.98
        }
        res = requests.post("http://34.93.184.130:5001/place-order", json=payload)
        assert res.status_code == 201
        print("Order Service POST OK")
    except Exception as e:
        print("Order Service POST Failed:", e)

# ----------- Test Game Service -----------
def test_game_service_get():
    """
    Test GET request to /games endpoint of game service.
    """
    try:
        res = requests.get("http://34.100.182.195:5000/games")
        assert res.status_code == 200
        print("Game Service GET OK")
    except Exception as e:
        print("Game Service GET Failed:", e)

def test_game_service_post():
    """
    Test POST request to /add-game endpoint.
    """
    try:
        payload = {
            "name": "Call of Duty 13",
            "category": "Action",
            "release_date": "2022-11-13",
            "price": 69.99
        }
        res = requests.post("http://34.100.182.195:5000/add-game", json=payload)
        assert res.status_code == 201
        print("Game Service POST OK")
    except Exception as e:
        print("Game Service POST Failed:", e)

# ----------- Test Analytics Service -----------
def test_analytics_service():
    """
    Test POST request to /track analytics endpoint.
    """
    try:
        payload = {
            "event_type": "integration_test",
            "page_url": "/test"
        }
        res = requests.post("http://35.200.226.132:5002/track", json=payload)
        assert res.status_code in [200, 201]
        print("Analytics Service Track OK")
    except Exception as e:
        print("Analytics Service Track Failed:", e)

# ----------- Test Frontend -----------
def test_frontend():
    """
    Test the frontend availability.
    """
    try:
        res = requests.get("http://35.244.41.165/")
        assert res.status_code == 200
        print("Frontend OK")
    except Exception as e:
        print("Frontend Failed:", e)

# ----------- Main Test Runner -----------
if __name__ == "__main__":
    test_order_service_get()
    test_order_service_post()
    test_game_service_get()
    test_game_service_post()
    test_analytics_service()
    test_frontend()
