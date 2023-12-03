from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram_interactions_service.states.registration_states import RegistrationForm
from telegram_interactions_service.middlewares.registration_middleware import IsUnregisteredMiddleware
from telegram_interactions_service.misc.dataclasses import InputUserData
from telegram_interactions_service.exceptions import BadRegistrationInput
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction
from typing import NoReturn

registration_router = Router()


@registration_router.message(Command("reg"))
async def cmd_reg(message: Message, state: FSMContext) -> NoReturn:
    await message.answer("Привет! Введите ваше имя:")
    await state.set_state(RegistrationForm.name)


@registration_router.message(Command("cancel"))
@registration_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> NoReturn:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Регистрация прервана!")


@registration_router.message(RegistrationForm.name)
async def receive_name(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(name=message.text)
    await state.set_state(RegistrationForm.surname)
    await message.answer("Введите вашу фамилию:")


@registration_router.message(RegistrationForm.surname)
async def receive_surname(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(surname=message.text)
    await state.set_state(RegistrationForm.group)
    await message.answer("Введите свою группу:")


@registration_router.message(RegistrationForm.group)
async def receive_group(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(group=message.text)
    await state.set_state(RegistrationForm.email_address)
    await message.answer("Введите свою электронную почту физтеха:")


@registration_router.message(RegistrationForm.email_address)
async def receive_email_address(message: Message, state: FSMContext) -> NoReturn:
    user_data = await state.get_data()
    await state.clear()
    try:
        user = InputUserData(**user_data, email_address=message.text, tg_id=message.from_user.id)
    except BadRegistrationInput as error:
        await message.answer("Данные введены в неверном формате! Пройдите регистрацию заново!")
        return
    user_managing_service = UserManagingServiceInteraction()
    await user_managing_service.add_user_to_database(user)
    await message.answer(f"{user_data['name'].capitalize()}, Вы успешно зарегистрированы!")


def setup(*, dispatcher: Dispatcher):
    registration_router.message.middleware(IsUnregisteredMiddleware())
    dispatcher.include_router(registration_router)
