from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/")
async def get_answer(req: Request):
    data = await req.json()
    query = data.get("question", "")
    return {"answer": f"You asked: '{query}'. This is a smart placeholder. Real legal brain incoming."}
