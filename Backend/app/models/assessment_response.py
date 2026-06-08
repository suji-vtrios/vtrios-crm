from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import Float

from app.database import Base


class AssessmentResponse(Base):

    __tablename__ = "assessment_responses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(Integer)

    question_id = Column(Integer)

    response = Column(Text)

    score = Column(
        Float,
        default=0
    )

    feedback = Column(Text)