class InvalidTokenException(Exception):
    """Вызывается если нет токена"""
    pass


class InvalidChatIDException(Exception):
    """Вызывается если нет chat ID"""
    pass


class APIUnavailable(Exception):
    """Вызывается если статус ответа сервера API отличается от 200OK"""
    pass


class WrongURL(Exception):
    """Вызывается если передано некорректное значение вместо URL"""
    pass
