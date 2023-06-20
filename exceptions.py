class InvalidTokenException(Exception):
    """Вызывается если нет токена"""
    def __int__(self, message='Некорректный токен'):
        self.message=message
        super(InvalidTokenDataException, self).__init__(self.message)


class InvalidChatIDException(Exception):
    """Вызывается если нет chat ID"""
    def __int__(self, message='Некорректный chat ID'):
        self.message = message
        super(InvalidChatIDException, self).__int__(self.message)


class APIUnavailable(Exception):
    """Вызывается если статус ответа сервера API отличается от 200OK"""
    pass

class WrongURL(Exception):
    """Вызывается если передано некорректное значение вместо URL"""
    pass
