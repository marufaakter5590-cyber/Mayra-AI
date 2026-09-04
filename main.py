import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mayra AI")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "assistant": "Mayra AI",
        "status": "online"
    }

@app.get("/healthz")
def health():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        return {"reply": "কিছু লিখুন।"}

    return {
        "reply": f"মায়রা বলছে: আপনি লিখেছেন — {message}"
    }
