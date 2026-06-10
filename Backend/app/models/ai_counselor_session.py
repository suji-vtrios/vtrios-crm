
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

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