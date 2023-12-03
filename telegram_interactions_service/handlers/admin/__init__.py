from aiogram import Router, Dispatcher
from typing import List
from . import general, material_help, user_manage, notify_service


def setup(*, dispatcher: Dispatcher):
    general.setup(dispatcher=dispatcher)
    # material_help.setup(dispatcher=dispatcher)
    notify_service.setup(dispatcher=dispatcher)
    user_manage.setup(dispatcher=dispatcher)
