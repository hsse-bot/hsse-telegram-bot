class BotException(Exception):
    pass


class BadRegistrationInput(BotException):
    pass


class EmailAlreadyUsed(BotException):
    pass


class TelegramNotifierServiceError(BotException):
    pass


class UserManagingServiceError(BotException):
    pass
