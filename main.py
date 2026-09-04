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
        return {"reply": "কিছু লিখুন, বস 😊"}

    api_key = os.getenv("MISTRAL_API_KEY")

    if not api_key:
        return {"reply": "Mistral API key সেট করা হয়নি।"}

    try:
        client = Mistral(api_key=api_key)

        response = client.chat.complete(
            model="mistral-small-latest",
            messages=[
                {
                    "role": "system",
                    "content": "তুমি Mayra AI। তুমি বাংলায় বন্ধুসুলভভাবে উত্তর দেবে এবং ব্যবহারকারীকে বস বলে ডাকবে।"
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = response.choices[0].message.content

        return {"reply": reply}

    except Exception as error:
        return {
            "reply": f"দুঃখিত বস, একটু সমস্যা হয়েছে: {str(error)}"
        }
