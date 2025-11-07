from aiogram.exceptions import DetailedAiogramError


class UserNotFoundError(DetailedAiogramError):
    def __init__(self) -> None:
        self.message: str = '❗️ Пользователь не найден!'
        super().__init__(message=self.message)
