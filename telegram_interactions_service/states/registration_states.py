from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    name = State()
    surname = State()
    group = State()
    email_address = State()
