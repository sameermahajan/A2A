import requests
import time


class SimpleA2AClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.capabilities = None

    # ----------------------------
    # 1. Discovery
    # ----------------------------
    def discover(self):
        print("\n[DISCOVERY] Fetching agent card...")

        r = requests.get(f"{self.base_url}/agent", timeout=5)
        r.raise_for_status()

        self.capabilities = r.json()

        print("[DISCOVERY] Agent name:", self.capabilities.get("name"))
        print("[DISCOVERY] Capabilities:")

        for cap in self.capabilities.get("capabilities", []):
            print("  -", cap["name"])

        return self.capabilities

    # ----------------------------
    # 2. Select capability
    # ----------------------------
    def get_chat_capability(self):
        if not self.capabilities:
            raise Exception("Call discover() first")

        for cap in self.capabilities["capabilities"]:
            if cap["name"].lower() in ["chat", "conversation", "ask"]:
                return cap["name"]

        raise Exception("No chat capability found")

    # ----------------------------
    # 3. Invoke (create task)
    # ----------------------------
    def create_task(self, capability, message, history):

        print("\n[INVOKE] Creating task...")

        payload = {
            "capability": capability,
            "input": {
                "message": message,
                "history": history
            }
        }

        r = requests.post(
            f"{self.base_url}/tasks",
            json=payload,
            timeout=5
        )

        r.raise_for_status()

        data = r.json()

        task_id = data.get("task_id")

        if not task_id:
            raise Exception(f"Invalid task response: {data}")

        print(f"[INVOKE] Task created: {task_id}")

        return task_id

    # ----------------------------
    # 4. Poll for result
    # ----------------------------
    def wait_for_result(self, task_id, timeout=20):

        print("\n[POLL] Waiting for completion...")

        start = time.time()

        while True:
            r = requests.get(
                f"{self.base_url}/tasks/{task_id}",
                timeout=5
            )

            r.raise_for_status()

            data = r.json()
            status = data.get("status")

            print(f"[POLL] Status: {status}")

            if status == "completed":
                return data.get("output")

            if status == "failed":
                raise Exception(f"Task failed: {data}")

            if time.time() - start > timeout:
                raise TimeoutError("Task timed out")

            time.sleep(0.5)

    # ----------------------------
    # 5. Parse response
    # ----------------------------
    def parse_response(self, output):

        print("\n[PARSE] Raw output:", output)

        if not output:
            raise Exception("Empty output")

        reply = output.get("reply")
        confidence = output.get("confidence")

        print("[PARSE] Reply:", reply)
        print("[PARSE] Confidence:", confidence)

        return reply

    # ----------------------------
    # Full flow
    # ----------------------------
    def chat(self, message, history=None):

        if history is None:
            history = []

        # discovery
        self.discover()

        # capability selection
        capability = self.get_chat_capability()
        print(f"[CAPABILITY] Using: {capability}")

        # invoke
        task_id = self.create_task(capability, message, history)

        # poll
        output = self.wait_for_result(task_id)

        # parse
        return self.parse_response(output)


# ----------------------------
# Demo run
# ----------------------------
if __name__ == "__main__":

    client = SimpleA2AClient("http://localhost:8002")

    reply = client.chat("hello")

    print("\n=== FINAL RESPONSE ===")
    print(reply)