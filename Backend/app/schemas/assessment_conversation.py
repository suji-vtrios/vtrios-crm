from pydantic import BaseModel


class ConversationReply(

    BaseModel
):

    session_id: int

    question_id: int

    answer: str