
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import Text

from app.database import Base


class AICounselorSession(Base):

    __tablename__ = "ai_counselor_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    lead_id = Column(
        Integer
    )

    status = Column(
        String,
        default="Active"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    lead_quality = Column(
        String
    )

    lead_intent = Column(
        String
    )

    education = Column(
        Text
    )

    experience = Column(
        Text
    )

    career_goal = Column(
        Text
    )