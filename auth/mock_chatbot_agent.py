from fastapi import FastAPI, Request, HTTPException
import uuid
import asyncio

app = FastAPI()

API_KEY = "super-secret-key"

# in-memory task store
tasks = {}


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
# Background task processor
# ----------------------------
async def process_task(task_id, message):

    # simulate async processing
    await asyncio.sleep(2)

    if "hello" in message.lower():
        reply = "Hi! How can I help you?"
    else:
        reply = f"You said: {message}"

    tasks[task_id]["status"] = "completed"

    tasks[task_id]["output"] = {
        "reply": reply
    }


# ----------------------------
# Create task
# ----------------------------
@app.post("/tasks")
async def create_task(request: Request):

    verify_auth(request)

    body = await request.json()

    capability = body.get("capability")

    if capability != "chat":
        return {
            "status": "failed",
            "error": "Unsupported capability"
        }

    message = body["input"]["message"]

    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "running",
        "output": None
    }

    # async background execution
    asyncio.create_task(
        process_task(task_id, message)
    )

    return {
        "task_id": task_id,
        "status": "submitted"
    }


# ----------------------------
# Poll task result
# ----------------------------
@app.get("/tasks/{task_id}")
async def get_task(task_id: str, request: Request):

    verify_auth(request)

    task = tasks.get(task_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "task_id": task_id,
        "status": task["status"],
        "output": task["output"]
    }