from fastapi import FastAPI
import time
import random

app = FastAPI()

fake_db = {
    "users": ["alice", "bob", "charlie"],
    "items": ["laptop", "phone", "keyboard"]
}

@app.get("/")
def root():
    return {"message": "Test app is running"}

@app.get("/users")
def get_users():
    time.sleep(random.uniform(0.1, 0.5))  # simulate latency
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