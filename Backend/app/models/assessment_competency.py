from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.database import Base


class AssessmentCompetency(Base):
    __tablename__ = "assessment_competencies"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    subcategory_id = Column(
        Integer,
        ForeignKey(
            "assessment_subcategories.id"
        )
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String
    )

    weight = Column(
        Integer,
        default=1
    )

    is_active = Column(
        Boolean,
        default=True
    )