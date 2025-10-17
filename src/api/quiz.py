from logging import Logger, getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.bll.filters.answer_options import InAnswerOptionsFilter
from src.bll.filters.right_answer import RightAnswerFilter
from src.bll.quiz import QuizService

logger: Logger = getLogger(__name__)

router: Router = Router(name=__name__)


# F.content_type == ContentType.DOCUMENT
# F.document & F.caption
# F.caption & (F.photo | F.video | F.document)


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    await quiz_service.add_gamer(message)

    await message.answer(
        'Привет! Готов проверить знания?',
        reply_markup=await quiz_service.get_kb(),
    )


@router.message(F.text, RightAnswerFilter())
async def right_answer(message: Message) -> None:
    await message.answer('OK')


@router.message(F.text, InAnswerOptionsFilter())
async def in_answer_options(message: Message) -> None:
    await message.answer('Неверный ответ!')


@router.message(F.text)
async def random_text(message: Message) -> None:
    await message.answer('Нет такого варианта!')


@router.message(~F.text)
async def other_handler(message: Message) -> None:
    await message.answer('🛑 Данный тип сообщения не обрабатывается!')
