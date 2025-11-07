from pydantic import BaseModel, RootModel


class Question(BaseModel):
    text: str
    answer_options: list[str]
    right_answer: str


class QuestionsValidator(RootModel[dict[int, Question]]):
    pass
