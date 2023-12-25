from aiogram.fsm.state import State, StatesGroup


class NotifySendTextForm(StatesGroup):
    text = State()


class CreateCategoryForm(StatesGroup):
    name = State()
