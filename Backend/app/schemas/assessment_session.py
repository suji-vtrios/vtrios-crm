from pydantic import BaseModel


class AssessmentSessionBase(
    BaseModel
):

    lead_id: int

    specialization: str

    status: str = "Pending"


class AssessmentSessionCreate(
    AssessmentSessionBase
):
    pass


class AssessmentSession(
    AssessmentSessionBase
):

    id: int

    overall_score: float | None = 0

    recommendation: str | None = None

    class Config:
        from_attributes = True