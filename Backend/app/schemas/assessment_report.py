from pydantic import BaseModel


class AssessmentReportBase(
    BaseModel
):

    session_id: int

    overall_score: float

    strengths: str | None = None

    weaknesses: str | None = None

    recommendation: str | None = None

    gpt_feedback: str | None = None


class AssessmentReportCreate(
    AssessmentReportBase
):
    pass


class AssessmentReport(
    AssessmentReportBase
):

    id: int

    class Config:

        from_attributes = True