from pydantic import BaseModel


class AssessmentQuestionBase(
    BaseModel
):
    competency_id: int

    question: str

    stream: str = "Common"

    difficulty: int = 1

    question_type: str = "Knowledge"

    expected_keywords: str | None = None

    scoring_guidance: str | None = None

    source: str = "Vtrios"

    is_active: bool = True


class AssessmentQuestionCreate(
    AssessmentQuestionBase
):
    pass


class AssessmentQuestion(
    AssessmentQuestionBase
):
    id: int

    class Config:
        from_attributes = True