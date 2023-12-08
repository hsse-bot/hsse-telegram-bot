from typing import NoReturn

from aiogram import Router, F, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from telegram_interactions_service.exceptions import BadRegistrationInput, EmailAlreadyUsed
from telegram_interactions_service.middlewares.registration_middleware import IsUnregisteredMiddleware
from telegram_interactions_service.misc import message_templates
from telegram_interactions_service.misc.dataclasses import RegistrationUserData
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction
from telegram_interactions_service.states.registration_states import RegistrationForm
from telegram_interactions_service.keyboards.inline import user

registration_router = Router()


@registration_router.callback_query(user.RegistrationKb.filter(F.action == "/cancel"))
async def call_cancel(callback: CallbackQuery, state: FSMContext) -> NoReturn:
    current_state = await state.get_state()
    if current_state is None:
        await callback.answer()
        return
    await state.clear()
    await callback.message.answer("Регистрация прервана!")
    await callback.answer()


@registration_router.message(Command("reg"))
async def cmd_reg(message: Message, state: FSMContext) -> NoReturn:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer("Вы прервали регистрацию! Нажмите /reg, чтобы начать регистрацию заново")
        return
    await message.answer("Привет! Введите ваше имя:", reply_markup=user.cancel_registration_kb())
    await state.set_state(RegistrationForm.name)


@registration_router.message(RegistrationForm.name)
async def receive_name(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(name=message.text)
    await state.set_state(RegistrationForm.surname)
    await message.answer("Введите вашу фамилию:", reply_markup=user.cancel_registration_kb())


@registration_router.message(RegistrationForm.surname)
async def receive_surname(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(surname=message.text)
    await state.set_state(RegistrationForm.group)
    await message.answer("Введите свою группу:", reply_markup=user.cancel_registration_kb())


@registration_router.message(RegistrationForm.group)
async def receive_group(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(group=message.text)
    await state.set_state(RegistrationForm.email_address)
    await message.answer("Введите свою электронную почту физтеха:", reply_markup=user.cancel_registration_kb())


@registration_router.message(RegistrationForm.email_address)
async def receive_email_address(message: Message, state: FSMContext) -> NoReturn:
    await state.update_data(email_address=message.text)
    user_registration_data = await state.get_data()
    await state.set_state(RegistrationForm.confirm_data)
    await message.answer("Подтвердите ваши данные:\n"
                         f"Имя: {user_registration_data['name']}\n"
                         f"Фамилия: {user_registration_data['surname']}\n"
                         f"Группа: {user_registration_data['group']}\n"
                         f"Элекстронная почта физтеха: {user_registration_data['email_address']}",
                         reply_markup=user.confirm_registration_kb())


@registration_router.callback_query(user.RegistrationKb.filter(F.action == "/confirm"))
async def call_confirm_registration_data(callback: CallbackQuery, state: FSMContext) -> NoReturn:
    current_state = await state.get_state()
    if current_state is None:
        await callback.answer()
        return
    user_data = await state.get_data()
    await state.clear()
    try:
        user_registration_data = RegistrationUserData(**user_data, tg_id=callback.from_user.id)
    except BadRegistrationInput as error:
        await callback.message.answer("Данные введены в неверном формате! Пройдите регистрацию заново!")
        await callback.answer()
        return
    try:
        user_managing_service = UserManagingServiceInteraction()
        await user_managing_service.add_user_to_database(user_registration_data)
    except EmailAlreadyUsed as error:
        await callback.message.answer(
            "Данный email адрес уже присутствует в системе! "
            "Используйте другой email или обратитесь к админимстратору"
        )
        await callback.answer()
        return
    except Exception as error:
        # TODO logs
        await callback.message.answer(message_templates.error_fail_to_reg)
        await callback.answer()
        return
    await callback.message.answer(f"{user_data['name'].capitalize()}, Вы успешно зарегистрированы!")
    await callback.answer()


def setup(*, dispatcher: Dispatcher):
    registration_router.message.middleware(IsUnregisteredMiddleware())
    dispatcher.include_router(registration_router)
