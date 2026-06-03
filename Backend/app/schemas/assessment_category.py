from pydantic import BaseModel


class AssessmentCategoryBase(BaseModel):
    name: str
    description: str | None = None
    display_order: int = 0
    is_active: bool = True


class AssessmentCategoryCreate(
    AssessmentCategoryBase
):
    pass


class AssessmentCategory(
    AssessmentCategoryBase
):
    id: int

    class Config:
        from_attributes = True