import logging

from aiogram import F, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram import Router
from aiogram.fsm.context import FSMContext

from telegram_interactions_service.misc import message_templates
from telegram_interactions_service.middlewares import IsAdminMiddleware
from telegram_interactions_service.keyboards.inline import admin
from telegram_interactions_service.misc.constants import ADMIN_MENU_COMMAND
from telegram_interactions_service.services_interactions.user_managing_service import UserManagingServiceInteraction
from telegram_interactions_service.states.give_points_states import GivePointsForm

admin_general_router = Router()
logger = logging.getLogger(__name__)


@admin_general_router.message(Command(ADMIN_MENU_COMMAND))
async def cmd_menu(message: Message, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await message.answer("Админ панель", reply_markup=admin.admin_main_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/"))
async def call_admin_menu(callback: CallbackQuery, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await callback.message.edit_text("Админ панель", reply_markup=admin.admin_main_kb())


# @admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/material_help"))
# async def call_material_help_menu(callback: CallbackQuery):
#     await callback.message.edit_text("Меню сервиса матпомощи", reply_markup=admin.admin_material_help_menu_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/notify_service"))
async def call_notify_service_menu(callback: CallbackQuery):
    await callback.message.edit_text("Меню сервиса уведомлений", reply_markup=admin.admin_notify_service_menu_kb())


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/get_users"))
async def call_get_users(callback: CallbackQuery):
    try:
        all_users = await UserManagingServiceInteraction().get_all_users()
        result = '\n'.join([f"{user.name} {user.surname} {user.tg_id} {user.score}" for user in all_users])
        await callback.message.edit_text(text="Имя Фамилия Telegram id Очки\n" + result,
                                         reply_markup=admin.return_main_menu())
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await callback.message.edit_text(message_templates.error_admin_text,
                                         reply_markup=admin.return_main_menu())
        await callback.answer()


@admin_general_router.callback_query(admin.AdminMainMenuKb.filter(F.action == "/give_points"))
async def give_points(callback: CallbackQuery, callback_data: admin.AdminMainMenuKb, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    await state.set_state(GivePointsForm.user_id)
    await callback.message.edit_text(text="Введите почту того, кому хотите выдать очки",
                                     reply_markup=admin.return_main_menu())
    await callback.answer()


@admin_general_router.message(GivePointsForm.user_id)
async def receive_email_for_point(message: Message, state: FSMContext):
    input_email = message.text
    try:
        all_users = await UserManagingServiceInteraction().get_all_users()
        for user in all_users:
            if user.email == input_email:
                await state.update_data(user_id=user.tg_id)
                await state.set_state(GivePointsForm.points)
                await message.answer(text="Введите количество очков",
                                     reply_markup=admin.return_main_menu())
                return
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await state.clear()
        await message.answer(message_templates.error_admin_text, reply_markup=admin.return_main_menu())
        return
    await message.answer(text=f"Пользователь с почтой {input_email} не найден, попробуйте ввести ещё раз",
                         reply_markup=admin.return_main_menu())


@admin_general_router.message(GivePointsForm.points)
async def give_points(message: Message, state: FSMContext):
    points = message.text.strip()
    if not (points.isdigit() or (points.startswith('-') and points[1:].isdigit())):
        await message.answer("Вы ввели не целое число. Введите количество очков", reply_markup=admin.return_main_menu())
        return
    try:
        user_tg_id = (await state.get_data())['user_id']
        await UserManagingServiceInteraction().add_activity_points(user_tg_id, int(points))
        await message.answer(text=f"Вы успешно начислили {points} очков!",
                             reply_markup=admin.return_main_menu())
        await state.clear()
    except Exception as error:
        logger.log(level=logging.ERROR, msg=error, exc_info=True)
        await state.clear()
        await message.answer(message_templates.error_admin_text,
                             reply_markup=admin.return_main_menu())


def setup(*, dispatcher: Dispatcher):
    admin_general_router.message.middleware(IsAdminMiddleware())
    dispatcher.include_router(admin_general_router)
