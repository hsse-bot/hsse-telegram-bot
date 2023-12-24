from aiogram import Router, Dispatcher
from typing import List
from . import admin_manage, user_manage


def setup(*, dispatcher: Dispatcher):
    admin_manage.setup(dispatcher=dispatcher)
    user_manage.setup(dispatcher=dispatcher)

