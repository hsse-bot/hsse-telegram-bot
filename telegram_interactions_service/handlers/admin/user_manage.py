from aiogram import Router, F, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from telegram_interactions_service.middlewares import IsAdminMiddleware

user_manage_router = Router()


@user_manage_router.message(Command("ban"))
async def ban_user(message: Message):
    if len(message.text.split()) != 2:
        await message.answer("Неверное использование команды!")
        return
    to_ban_id = int(message.text.split()[1])
    # here ban user


def setup(*, dispatcher: Dispatcher):
    user_manage_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(user_manage_router)
