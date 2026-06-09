from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class AssessmentConversation(Base):

    __tablename__ = (
        "assessment_conversations"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey(
            "assessment_sessions.id"
        )
    )

    question_id = Column(
        Integer,
        ForeignKey(
            "assessment_questions.id"
        ),
        nullable=True
    )

    role = Column(
        String
    )

    message = Column(
        String
    )

    sequence_no = Column(
        Integer,
        default=1
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )