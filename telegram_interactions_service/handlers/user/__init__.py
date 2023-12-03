from aiogram import Router, Dispatcher
from typing import List
from . import general, notify_service, registration


def setup(*, dispatcher: Dispatcher):
    general.setup(dispatcher=dispatcher)
    # material_help.setup(dispatcher=dispatcher)
    notify_service.setup(dispatcher=dispatcher)
    registration.setup(dispatcher=dispatcher)
