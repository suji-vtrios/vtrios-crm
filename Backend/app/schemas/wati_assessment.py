from pydantic import BaseModel


class WatiAssessmentMessage(
    BaseModel
):

    phone: str

    message: str