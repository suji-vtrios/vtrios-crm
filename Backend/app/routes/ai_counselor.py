from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
def chat(
    payload: dict
):

    message = payload.get(
        "message"
    )

    return {

        "message":
        f"You said: {message}"
    }