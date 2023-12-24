import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router
from pydantic_core._pydantic_core import ValidationError

from telegram_interactions_service.misc import dataclasses, constants
from telegram_interactions_service.misc.utils import generate_user_profile_text
from telegram_interactions_service.middlewares import IsRegisteredMiddleware
from telegram_interactions_service.keyboards.inline import user
from telegram_interactions_service.services_interactions.user_managing_service import \
    UserManagingServiceInteraction
from telegram_interactions_service.misc import message_templates
from telegram_interactions_service.exceptions import BadRegistrationInput
from telegram_interactions_service.states.change_profile_states import ChangeFieldForm

profile_router = Router()
logger = logging.getLogger(__name__)


@profile_router.callback_query(user.UserMainMenuKb.filter(F.action == "/profile"))
async def rating_handler(callback: CallbackQuery, callback_data: user.ProfileChangeDataKb, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    user_data = await UserManagingServiceInteraction().get_user(callback.from_user.id)
    await callback.message.edit_text('Ваш профиль\n' + generate_user_profile_text(user_data),
                                     reply_markup=user.profile_menu_kb())
    await callback.answer()


@profile_router.callback_query(user.ProfileChangeDataKb.filter(F.action == "/"))
async def show_fields_to_change_handler(callback: CallbackQuery, callback_data: user.ProfileChangeDataKb, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    if len(constants.all_student_info_fields) == 0:
        await callback.message.edit_text(f"Пока что нет полей для изменений",
                                         reply_markup=user.error_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(constants.all_student_info_fields) - 1) // constants.MAX_PROFILE_FIELD_PER_PAGE, int(callback_data.page)
    await callback.message.edit_text(f"Выберите поле, которое хотите изменить {cur_page + 1}/{max_page + 1}",
                                     reply_markup=user.profile_change_data_paginator_kb(callback_data.page))
    await callback.answer()


@profile_router.callback_query(user.ProfileChangeDataKb.filter(F.action.in_(["/prev", "/next"])))
async def show_fields_to_change_pagination_handler(callback: CallbackQuery, callback_data: user.ProfileChangeDataKb, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    if len(constants.all_student_info_fields) == 0:
        await callback.message.edit_text(f"Пока что нет полей для изменений",
                                         reply_markup=user.error_kb())
        await callback.answer()
        return
    max_page, cur_page = (len(constants.all_student_info_fields) - 1) // constants.MAX_PROFILE_FIELD_PER_PAGE, int(callback_data.page)
    next_categories_page = cur_page
    if callback_data.action == "/next":
        if cur_page == max_page:
            await callback.answer()
            return
        next_categories_page = cur_page + 1 if cur_page < max_page else cur_page
    elif callback_data.action == "/prev":
        if cur_page == 0:
            await rating_handler(callback, callback_data, state)
            return
        next_categories_page = cur_page - 1
    await callback.message.edit_text(text=f"Выберите поле, которое хотите изменить {next_categories_page+1}/{max_page+1}",
                                     reply_markup=user.profile_change_data_paginator_kb(next_categories_page))
    await callback.answer()


@profile_router.callback_query(user.ProfileChangeDataKb.filter(F.action.startswith("/field/")))
async def enter_new_field_value_handler(callback: CallbackQuery, callback_data: user.NotifyCategoriesKb, state:FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    field_name = callback_data.action[7:]
    field_to_change = None
    for field in constants.all_student_info_fields:
        if field.db_name == field_name:
            field_to_change = field
    if field_to_change is not None:
        await state.update_data(field_db_name=field_to_change.db_name, field_output_name=field_to_change.output_name)
        await state.set_state(ChangeFieldForm.new_value)
        if field_to_change.db_name == 'isMale':
            await callback.message.answer(f"Введите {field_to_change.output_name}(м/ж):", reply_markup=user.cancel_data_changing_kb())
        else:
            await callback.message.answer(f"Введите {field_to_change.output_name}:", reply_markup=user.cancel_data_changing_kb())
        await callback.message.delete()
    else:
        logger.log(level=logging.ERROR, msg=f"unknown field'{callback_data.action}'")
        await callback.message.edit_text(message_templates.error_fail_to_change_field,
                                         reply_markup=user.error_kb())
        return


@profile_router.message(ChangeFieldForm.new_value)
async def change_field_handler(message: Message, state: FSMContext):
    await state.update_data(new_value=message.text)
    state_data = await state.get_data()
    await state.clear()
    if state_data['field_db_name'] == 'isMale':
        if state_data['new_value'].strip().lower() in ('м', 'ж'):
            state_data['new_value'] = state_data['new_value'].strip().lower() == 'м'
        else:
            await message.answer(f"Неверный формат ввода.",
                                 reply_markup=user.return_to_profile_kb())
            return
    try:
        if state_data['field_db_name'] == 'groupNumber':
            dataclasses.StudentInfoDelta.validate_group(state_data['new_value'])
        student_info_delta = dataclasses.generate_delta_student_info({state_data['field_db_name']: state_data['new_value']})
        # student_info_delta.validate({state_data['field_db_name']: state_data['new_value']})
    except (ValidationError, BadRegistrationInput) as error:
        await message.answer(f"Неверный формат ввода.",
                             reply_markup=user.return_to_profile_kb())
        return
    # except Exception:
    #     await message.answer(message_templates.error_fail_to_change_field,
    #                          reply_markup=user.error_kb())
    #     return
    try:
        user_delta = dataclasses.UserDelta()
        user_delta.studentInfoDelta = student_info_delta
        await UserManagingServiceInteraction().update_user(message.from_user.id, user_delta)
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await message.answer(message_templates.error_fail_to_change_field,
                             reply_markup=user.error_kb())
        return
    await message.answer(f"Вы успешно изменили {state_data['field_output_name']}", reply_markup=user.return_to_profile_kb())


def setup(*, dispatcher: Dispatcher):
    profile_router.message.middleware(IsRegisteredMiddleware())
    dispatcher.include_router(profile_router)
