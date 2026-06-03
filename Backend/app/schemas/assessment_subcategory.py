from pydantic import BaseModel


class AssessmentSubcategoryBase(
    BaseModel
):
    category_id: int
    name: str
    description: str | None = None
    display_order: int = 0
    is_active: bool = True


class AssessmentSubcategoryCreate(
    AssessmentSubcategoryBase
):
    pass


class AssessmentSubcategory(
    AssessmentSubcategoryBase
):
    id: int

    class Config:
        from_attributes = True