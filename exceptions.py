class InvalidTokenException(Exception):
    """Вызывается если нет токена"""
    pass


class InvalidChatIDException(Exception):
    """Вызывается если нет chat ID"""
    pass


class APIUnavailable(Exception):
    """Вызывается если статус ответа сервера API отличается от 200OK"""
    pass


class RequestsError(Exception):
    """Вызывается если requests падают с ошибкой"""
    pass
