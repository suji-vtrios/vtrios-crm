from fastapi import APIRouter
from fastapi import Request

router = APIRouter()


@router.post("/webhook")
async def webhook(request: Request):

    payload = await request.json()

    print("================================")
    print("WATI WEBHOOK RECEIVED")
    print(payload)
    print("================================")

    return {
        "status": "ok"
    }