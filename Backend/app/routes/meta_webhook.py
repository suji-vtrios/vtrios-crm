from fastapi import APIRouter
from app.config import settings
import json

router = APIRouter()

@router.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):

    print(hub_mode)
    print(hub_verify_token)
    print(hub_challenge)

    if hub_verify_token == settings.META_VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Invalid token"}


@router.post("/webhook")
async def receive_lead(payload: dict):

    print("=" * 50)
    print(payload)
    print("=" * 50)

    with open(
        "meta_payload.json",
        "a"
    ) as f:

        f.write(
            json.dumps(payload)
        )

        f.write("\n")

    return {
        "status": "received"
    }

from app.models.lead import Lead
from app.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

@router.post("/test-lead")
def test_lead(
    db: Session = Depends(get_db)
):

    lead = Lead(

        name="Meta Test Lead",

        email="test@vtrios.com",

        phone="918891393010",

        source="Meta Test",

        status="New"
    )

    db.add(lead)

    db.commit()

    db.refresh(lead)

    return lead