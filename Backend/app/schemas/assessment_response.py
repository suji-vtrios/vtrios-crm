from pydantic import BaseModel


class AssessmentResponseBase(
    BaseModel
):

    session_id: int

    question_id: int

    response: str


class AssessmentResponseCreate(
    AssessmentResponseBase
):
    pass


class AssessmentResponse(
    AssessmentResponseBase
):

    id: int

    score: float | None = 0

    feedback: str | None = None

    class Config:
        from_attributes = True