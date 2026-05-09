# POST task like
# {
#  "capability": "chat",
#  "input": {
#    "message": "hello",
#    "history": []
#  }
# }
#
# to fetch response call something like
# curl http://localhost:8002/tasks/41f42b78-a084-4c35-85bd-dc43aedc474f
#
import uuid
import time
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Mock A2A Chatbot Agent")

# ----------------------------
# In-memory task store
# ----------------------------
tasks: Dict[str, dict] = {}


# ----------------------------
# Models
# ----------------------------
class TaskRequest(BaseModel):
    capability: str
    input: dict


# ----------------------------
# Agent Card (discovery)
# ----------------------------
@app.get("/agent")
def agent_card():
    return {
        "name": "mock-chatbot-agent",
        "description": "Simple mock chatbot for A2A testing",
        "capabilities": [
            {
                "name": "chat",
                "input_schema": {
                    "message": "string",
                    "history": "array"
                },
                "output_schema": {
                    "reply": "string"
                }
            }
        ]
    }


# ----------------------------
# Task creation
# ----------------------------
@app.post("/tasks")
def create_task(req: TaskRequest):

    if req.capability != "chat":
        return {"error": "Unsupported capability"}

    task_id = str(uuid.uuid4())

    tasks[task_id] = {
        "status": "running",
        "input": req.input,
        "output": None
    }

    # simulate async processing
    process_task(task_id)

    return {
        "task_id": task_id,
        "status": "submitted"
    }


# ----------------------------
# Task processing (mock logic)
# ----------------------------
def process_task(task_id):

    user_msg = tasks[task_id]["input"]["message"]

    # Simulate delay
    time.sleep(0.5)

    # Simple deterministic responses
    if "hello" in user_msg.lower():
        reply = "Hi! How can I help you today?"
    elif "order" in user_msg.lower():
        reply = "Your order is being processed."
    elif "bye" in user_msg.lower():
        reply = "Goodbye! Have a great day!"
    else:
        reply = f"You said: {user_msg}"

    tasks[task_id]["output"] = {
        "reply": reply,
        "confidence": 0.99
    }

    tasks[task_id]["status"] = "completed"


# ----------------------------
# Task status
# ----------------------------
@app.get("/tasks/{task_id}")
def get_task(task_id: str):

    task = tasks.get(task_id)

    if not task:
        return {"error": "Task not found"}

    return {
        "task_id": task_id,
        "status": task["status"],
        "output": task["output"]
    }