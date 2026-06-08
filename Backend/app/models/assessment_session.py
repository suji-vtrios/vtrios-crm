from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from app.database import Base


class AssessmentSession(Base):

    __tablename__ = "assessment_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    lead_id = Column(Integer)

    status = Column(
        String,
        default="Pending"
    )

    specialization = Column(String)

    overall_score = Column(
        Float,
        default=0
    )

    recommendation = Column(String)