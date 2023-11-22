class BotException(Exception):
    pass


class BadRegistrationInput(BotException):
    pass


class TelegramNotifierServiceError(BotException):
    pass
