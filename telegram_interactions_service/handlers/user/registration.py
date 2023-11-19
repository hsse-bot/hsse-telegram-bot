from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

registration_router = Router()


@registration_router.message(Command("reg"))
async def cmd_hello(message: Message):
    await message.answer("Привет мир!")


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(registration_router)
