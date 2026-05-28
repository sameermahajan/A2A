from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

API_KEY = "Sameer-TalentNovo"


# ----------------------------
# Auth helper
# ----------------------------
def verify_auth(request: Request):

    auth = request.headers.get("Authorization")

    if auth != f"Bearer {API_KEY}":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )


# ----------------------------
# Discovery endpoint
# ----------------------------
@app.get("/agent")
def agent():

    return {
        "name": "mock-chatbot-agent",
        "capabilities": [
            {
                "name": "chat"
            }
        ]
    }


# ----------------------------
# Chat endpoint
# ----------------------------
@app.post("/tasks")
async def tasks(request: Request):

    verify_auth(request)

    body = await request.json()

    capability = body.get("capability")

    if capability != "chat":
        return {
            "status": "failed",
            "error": "Unsupported capability"
        }

    message = body["input"]["message"]

    # simple mock logic
    if "hello" in message.lower():
        reply = "Hi! How can I help you?"
    else:
        reply = f"You said: {message}"

    return {
        "status": "completed",
        "output": {
            "reply": reply
        }
    }