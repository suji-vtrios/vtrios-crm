from fastapi import APIRouter

router = APIRouter()


@router.post("/webhook")
async def webhook(
    payload: dict
):

    print("=" * 50)
    print(payload)
    print("=" * 50)

    return {
        "status": "received"
    }