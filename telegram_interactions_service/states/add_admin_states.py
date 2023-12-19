from aiogram.fsm.state import State, StatesGroup


class AddAdminForm(StatesGroup):
    tg_id = State()
