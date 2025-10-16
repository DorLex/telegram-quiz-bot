from aiogram import Router

from src.api import quiz

bot_router: Router = Router(name=__name__)

bot_router.include_router(quiz.router)
