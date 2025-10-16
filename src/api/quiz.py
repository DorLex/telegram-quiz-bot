from logging import Logger, getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

logger: Logger = getLogger(__name__)

router: Router = Router(name=__name__)


# F.content_type == ContentType.DOCUMENT
# F.document & F.caption
# F.caption & (F.photo | F.video | F.document)


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer('Привет)')


@router.message(F.text)
async def text_handler(message: Message) -> None:
    await message.answer(message.text)


@router.message()
async def other_handler(message: Message) -> None:
    await message.answer('🛑 Данный тип сообщения не обрабатывается!')
