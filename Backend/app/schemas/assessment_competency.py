from pydantic import BaseModel


class AssessmentCompetencyBase(
    BaseModel
):
    subcategory_id: int
    name: str
    description: str | None = None
    weight: int = 1
    is_active: bool = True


class AssessmentCompetencyCreate(
    AssessmentCompetencyBase
):
    pass


class AssessmentCompetency(
    AssessmentCompetencyBase
):
    id: int

    class Config:
        from_attributes = True