from aiogram import Bot, Router, Dispatcher
from aiogram.utils.i18n import I18n
from telegram_interactions_service import config

router = Router()


@router.startup()
async def on_startup(bot: Bot):
    await bot.set_webhook(
        url=config.WEBHOOK_URL.format(bot_token=bot.token),
        secret_token=config.SECRET_KEY,
        drop_pending_updates=True,
    )


@router.shutdown()
async def on_shutdown(bot: Bot):
    await bot.delete_webhook(
        drop_pending_updates=True,
    )


def setup(*, dispatcher: Dispatcher):
    dispatcher.include_router(router)
