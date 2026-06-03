from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey
)

from app.database import Base


class AssessmentSubcategory(Base):
    __tablename__ = "assessment_subcategories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    category_id = Column(
        Integer,
        ForeignKey(
            "assessment_categories.id"
        )
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