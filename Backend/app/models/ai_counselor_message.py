from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base


class AICounselorMessage(Base):

    __tablename__ = "ai_counselor_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer
    )

    role = Column(
        String
    )

    message = Column(
        Text
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )