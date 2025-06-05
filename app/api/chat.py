from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import os
from openai import OpenAI

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.options("/chat")
async def options_handler():
    return JSONResponse(status_code=200)

@router.post("/chat")
async def chat_handler(request: Request):
    body = await request.json()
    query = body.get("query")

    if not query:
        return JSONResponse(content={"error": "No query provided."}, status_code=400)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful legal assistant specialised in Indian military law."},
            {"role": "user", "content": query}
        ]
    )

    return {"response": response.choices[0].message.content}
