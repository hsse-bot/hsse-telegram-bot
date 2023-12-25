from aiogram.fsm.state import State, StatesGroup


class GivePointsForm(StatesGroup):
    user_id = State()
    points = State()

