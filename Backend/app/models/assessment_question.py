from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text
)

from app.database import Base


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    competency_id = Column(
        Integer,
        ForeignKey(
            "assessment_competencies.id"
        )
    )

    question = Column(
        Text,
        nullable=False
    )

    stream = Column(
        String,
        default="Common"
    )

    difficulty = Column(
        Integer,
        default=1
    )

    question_type = Column(
        String,
        default="Knowledge"
    )

    expected_keywords = Column(
        Text
    )

    scoring_guidance = Column(
        Text
    )

    source = Column(
        String,
        default="Vtrios"
    )

    is_active = Column(
        Boolean,
        default=True
    )