import os
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

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
        return {"reply": "কিছু লিখুন"}

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {"reply": "Gemini API key সেট করা হয়নি।"}

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=message
        )

        return {
            "reply": response.text
        }

    except Exception:
        return {
            "reply": "দুঃখিত, এখন উত্তর দিতে সমস্যা হচ্ছে।"
        }
