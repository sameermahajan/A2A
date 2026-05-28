import requests

BASE_URL = "http://localhost:8001"

API_KEY = "Sameer-TalentNovo"
# API_KEY = "Wrong-Key"

# ----------------------------
# Discovery
# ----------------------------
print("\n=== DISCOVERY ===")

card = requests.get(
    f"{BASE_URL}/agent"
)

print(card.json())


# ----------------------------
# Invocation
# ----------------------------
print("\n=== INVOCATION ===")

payload = {
    "capability": "chat",
    "input": {
        "message": "hello"
    }
}

response = requests.post(
    f"{BASE_URL}/tasks",
    json=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

print(response.json())
