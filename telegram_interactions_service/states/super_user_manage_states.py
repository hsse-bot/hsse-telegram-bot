from aiogram.fsm.state import State, StatesGroup


class BanUserForm(StatesGroup):
    tg_id = State()


class DeleteUserForm(StatesGroup):
    tg_id = State()


class UnbanUserForm(StatesGroup):
    tg_id = State()
