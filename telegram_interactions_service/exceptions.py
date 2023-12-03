class BotException(Exception):
    pass


class BadRegistrationInput(BotException):
    pass


class EmailAlreadyUsed(BotException):
    pass
