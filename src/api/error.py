from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

from src.bll.exceptions.user import UserNotFoundError

router: Router = Router(name=__name__)


@router.error(ExceptionTypeFilter(UserNotFoundError), F.update.message.as_('message'))
async def user_not_found(event: ErrorEvent, message: Message) -> None:
    exc: UserNotFoundError = event.exception
    await message.answer(exc.message)
