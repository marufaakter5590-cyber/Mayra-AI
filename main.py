import os
from fastapi import FastAPI
from pydantic import BaseModel
from mistralai.client import Mistral

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

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        return {"reply": "Mistral API key সেট করা হয়নি।"}

    try:
        client = Mistral(api_key=api_key)

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as e:
        return {
            "reply": "দুঃখিত, এখন উত্তর দিতে সমস্যা হচ্ছে।"
        }
