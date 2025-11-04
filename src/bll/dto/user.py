from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    name: str
    question_id: int
    score: int
