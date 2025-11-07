from logging import Logger, getLogger

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiosqlite import Connection

from src.bll.dto.user import UserDTO
from src.bll.filters.answer_options import InAnswerOptionsFilter
from src.bll.filters.right_answer import RightAnswerFilter
from src.bll.quiz import QuizService
from src.core.constants import START_MSG, WELCOME_MSG, EndKeyboardEnum
from src.dal.quiz import QuizRepository

logger: Logger = getLogger(__name__)

router: Router = Router(name=__name__)


@router.message(CommandStart())
async def command_start(message: Message, db: Connection) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    await quiz_service.add_gamer(message)

    await message.answer(
        WELCOME_MSG,
        reply_markup=quiz_service.get_welcome_keyboard(),
    )


@router.message(F.text.contains(START_MSG))
async def start_quiz(message: Message, db: Connection) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    user: UserDTO = await quiz_service.get_user(message)
    text_question, keyboard = await quiz_service.get_current_question(user)

    await message.answer(
        text_question,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.show_result))
async def show_result(message: Message, db: Connection) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    user: UserDTO = await quiz_service.get_user(message)
    result, keyboard = await quiz_service.show_result(user)

    await message.answer(
        result,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.show_leaderboard))
async def show_leaderboard(message: Message, db: Connection) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    leaderboard, keyboard = await quiz_service.show_leaderboard()

    await message.answer(
        leaderboard,
        reply_markup=keyboard,
    )


@router.message(F.text.contains(EndKeyboardEnum.new_game))
async def new_game(message: Message, db: Connection) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    text, keyboard = await quiz_service.new_game(message)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text, RightAnswerFilter())
async def right_answer(message: Message, db: Connection, user: UserDTO) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    text, keyboard = await quiz_service.add_point(user)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text, InAnswerOptionsFilter())
async def in_answer_options(message: Message, db: Connection, user: UserDTO) -> None:
    quiz_service: QuizService = QuizService(QuizRepository(db))
    text, keyboard = await quiz_service.next_question(user)

    await message.answer(
        text,
        reply_markup=keyboard,
    )


@router.message(F.text)
async def random_text(message: Message) -> None:
    await message.answer('🤷‍♂️ Нет такого варианта!')


@router.message(~F.text)
async def other_handler(message: Message) -> None:
    await message.answer('🛑 Данный тип сообщения не обрабатывается!')
