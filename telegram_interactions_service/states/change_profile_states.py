from aiogram.fsm.state import State, StatesGroup


class ChangeFieldForm(StatesGroup):
    field_db_name = State()
    field_output_name = State()
    new_value = State()

