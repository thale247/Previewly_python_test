from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import time
import random
import os

app = FastAPI()

ENV_NAME = os.getenv("ENV_NAME", "dev")

fake_db = {
    "users": ["alice", "bob", "charlie"],
    "items": ["laptop", "phone", "keyboard"]
}

@app.get("/", response_class=HTMLResponse)
def homepage():
    return f"""
    <html>
        <head>
            <title>Test PR Environment</title>
            <style>
                body {{ font-family: Arial; margin: 40px; }}
                button {{ margin: 5px; padding: 10px; }}
                #output {{ margin-top: 20px; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h1>🚀 Test Environment: {ENV_NAME}</h1>
            <p>This simulates a PR preview environment.</p>

            <button onclick="callApi('/users')">Get Users</button>
            <button onclick="callApi('/items')">Get Items</button>
            <button onclick="callApi('/slow')">Slow Request</button>
            <button onclick="callApi('/error')">Trigger Error</button>
            <button onclick="callApi('/compute')">Compute</button>

            <div id="output"></div>

            <script>
                async function callApi(path) {{
                    const output = document.getElementById("output");
                    output.innerText = "Loading...";

                    try {{
                        const res = await fetch(path);
                        const text = await res.text();
                        output.innerText = text;
                    }} catch (err) {{
                        output.innerText = "Error: " + err;
                    }}
                }}
            </script>
        </body>
    </html>
    """



@app.get("/users")
def get_users():
    time.sleep(random.uniform(0.1, 0.5))
    return {"users": fake_db["users"]}

@app.get("/items")
def get_items():
    time.sleep(random.uniform(0.2, 1.0))
    return {"items": fake_db["items"]}

@app.get("/slow")
def slow_endpoint():
    delay = random.uniform(1, 3)
    time.sleep(delay)
    return {"message": f"Slow response: {delay:.2f}s"}

@app.get("/error")
def error_endpoint():
    if random.random() < 0.5:
        raise Exception("Random failure occurred")
    return {"message": "No error this time"}

@app.get("/compute")
def compute(n: int = 1000000):
    total = 0
    for i in range(n):
        total += i
    return {"result": total}

@app.get("/env")
def env():
    return {"env": ENV_NAME}