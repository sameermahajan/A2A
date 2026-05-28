import requests
import time

BASE_URL = "http://localhost:8001"

API_KEY = "super-secret-key"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


# ----------------------------
# Discovery
# ----------------------------
print("\n=== DISCOVERY ===")

card = requests.get(
    f"{BASE_URL}/agent"
)

print(card.json())


# ----------------------------
# Create task
# ----------------------------
print("\n=== CREATE TASK ===")

payload = {
    "capability": "chat",
    "input": {
        "message": "hello"
    }
}

response = requests.post(
    f"{BASE_URL}/tasks",
    json=payload,
    headers=HEADERS
)

task_data = response.json()

print(task_data)

task_id = task_data["task_id"]


# ----------------------------
# Poll result
# ----------------------------
print("\n=== POLLING ===")

while True:

    r = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers=HEADERS
    )

    data = r.json()

    print(data)

    if data["status"] == "completed":
        break

    time.sleep(1)


print("\n=== FINAL RESPONSE ===")

print(data["output"]["reply"])