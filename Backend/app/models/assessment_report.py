from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from app.database import Base


class AssessmentReport(Base):

    __tablename__ = "assessment_reports"

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

    overall_score = Column(
        Float,
        default=0
    )

    strengths = Column(
        Text,
        nullable=True
    )

    weaknesses = Column(
        Text,
        nullable=True
    )

    recommendation = Column(
        String,
        nullable=True
    )

    gpt_feedback = Column(
        Text,
        nullable=True
    )