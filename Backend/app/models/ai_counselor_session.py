
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy import Text

from app.database import Base
from sqlalchemy import Boolean



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

    bim_familiarity = Column(
        Text
    )

    career_goal = Column(
        Text
    )

    recommended_course = Column(
        String
    )

    current_stage = Column(
        String,
        default="GREETING"
    )

    assessment_score = Column(
        Integer,
        default=0
    )

    assessment_completed = Column(
        Boolean,
        default=False
    )

    next_action = Column(
        String
    )

    objection_type = Column(
        String
    )

    enrollment_probability = Column(
        Integer,
        default=0
    )