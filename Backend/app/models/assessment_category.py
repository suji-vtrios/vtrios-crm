from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class AssessmentCategory(Base):
    __tablename__ = "assessment_categories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        String
    )

    display_order = Column(
        Integer,
        default=0
    )

    is_active = Column(
        Boolean,
        default=True
    )