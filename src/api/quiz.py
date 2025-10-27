from logging import Logger, getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.bll.filters.answer_options import InAnswerOptionsFilter
from src.bll.filters.right_answer import RightAnswerFilter
from src.bll.quiz import QuizService
from src.core.constants import START_MSG, EndKeyboardEnum

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
        reply_markup=quiz_service.get_welcome_keyboard(),
    )


@router.message(F.text.contains(START_MSG))
async def start_quiz(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    text_question, keyboard = await quiz_service.get_current_question(message)

    await message.answer(
        text_question,
        reply_markup=keyboard,
    )


@router.message(F.text, RightAnswerFilter())
async def right_answer(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    text, keyboard = await quiz_service.add_point(message)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text, InAnswerOptionsFilter())
async def in_answer_options(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    text, keyboard = await quiz_service.next_question(message)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.show_result))
async def show_result(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    result, keyboard = await quiz_service.show_result(message)

    await message.answer(
        result,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.show_leaderboard))
async def show_leaderboard(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    leaderboard, keyboard = await quiz_service.show_leaderboard()

    await message.answer(
        leaderboard,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.new_game))
async def new_game(message: Message) -> None:
    quiz_service: QuizService = QuizService()
    text, keyboard = await quiz_service.new_game(message)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text)
async def random_text(message: Message) -> None:
    await message.answer('Нет такого варианта!')


@router.message(~F.text)
async def other_handler(message: Message) -> None:
    await message.answer('🛑 Данный тип сообщения не обрабатывается!')
