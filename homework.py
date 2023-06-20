import logging
import os
import sys
import time
from http import HTTPStatus
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (APIUnavailable, InvalidChatIDException,
                        InvalidTokenException)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler('bot.log', maxBytes=1000000, backupCount=3)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def check_tokens():
    """Проверка токена и chat id."""
    try:
        if not TELEGRAM_TOKEN:
            raise InvalidTokenException('Не найден токен телеграма')
        if not TELEGRAM_CHAT_ID:
            raise InvalidChatIDException('Не найден chat ID')
        if not PRACTICUM_TOKEN:
            raise InvalidTokenException('Не найден токен практикума')
    except InvalidChatIDException as error:
        logger.critical(error, exc_info=True)
        sys.exit('Ошибка проверки chat ID')
    except InvalidTokenException as error:
        logger.critical(error, exc_info=True)
        if 'практикума' in str(error):
            send_message(message='Не найден токен практикума')
        sys.exit('Ошибка проверки токенов')


def send_message(bot=None, message=''):
    """Отправка сообщения в телеграм."""
    if not bot:
        bot = telegram.Bot(token=TELEGRAM_TOKEN)

    logger.debug(f'Отправляем сообщение "{message}" в телеграм')
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception as error:
        logger.error(error, exc_info=True)


def get_api_answer(timestamp):
    """Получение ответа от API Яндекс практикума."""
    params = {'from_date': timestamp}
    logger.debug(f'Отправка запроса к API Яндекс практикума {ENDPOINT}')
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            raise APIUnavailable
        return response.json()
    except requests.RequestException as error:
        logger.error(error, exc_info=True)
        send_message(message=f'Ошибка при запросе к API \n{error}')


def check_response(response):
    """Проверка ответа API Яндекса на соответствие ожидаемому."""
    logger.debug('Проверяем ответ API')

    if not isinstance(response, dict):
        raise TypeError('Полученный ответ не является словарем')
    if not response.get('homeworks'):
        raise KeyError('В словаре ответа нет ключа homeworks')

    if not isinstance(response['homeworks'], list):
        raise TypeError(
            'В словаре ответа по ключу homeworks не найден список с '
            'домашними работами'
        )
    if not isinstance(response['current_date'], int):
        raise TypeError(
            'В словаре ответа по ключу current_date не найдено время в '
            'формате UNIX'
        )


def parse_status(homework):
    """Извлечение статуса домашней работы."""
    logger.debug('Извлекаем статус домашней работы')
    if not homework.get('homework_name'):
        raise KeyError('Ключ "homework_name" отсутствует в словаре домашки')
    homework_name = homework['homework_name']
    if not homework.get('status'):
        raise KeyError('Ключ "status" отсутствует в словаре домашки')
    if not HOMEWORK_VERDICTS.get(homework['status']):
        raise KeyError('Некорректный статус домашки')
    verdict = HOMEWORK_VERDICTS[homework['status']]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            check_response(response)
            timestamp = response['current_date']
            for homework in response['homeworks']:
                status = parse_status(homework)
                send_message(bot, status)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(error, exc_info=True)
            send_message(bot, message)

        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
