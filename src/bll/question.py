import json
from pathlib import Path

from src.bll.dto.question import Question, QuestionsValidator
from src.core.constants import BASE_DIR


class QuestionsLoader:
    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path
        self.questions: dict[int, Question] | None = None

    def load(self) -> None:
        with open(self.file_path, encoding='utf-8') as file:
            file_data: dict = json.load(file)

        questions_validator: QuestionsValidator = QuestionsValidator.model_validate(file_data)
        self.questions = questions_validator.root


questions_loader: QuestionsLoader = QuestionsLoader(BASE_DIR / 'data/questions.json')
