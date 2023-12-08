# homework_bot
Простой телеграм бот на Python для проверки статуса домашнего задания на Яндекс Практикуме

## Запуск проекта локально:
1. Скачиваем проект с гитхаба
```commandline
git clone <ссылка на проект> <директория проекта>
```
2. Создаем виртуальное окружение в директории проекта
```commandline
cd <директория проекта>
python -m venv venv
```
3. Активируем виртуальное окружение
```commandline
source env/bin/activate
```
4. Обновляем pip
```commandline
python -m pip install --upgrade pip
```
5. Устанавливаем пакеты необходимые для проекта
```commandline
pip install -r requirements.txt
```
6. Создайте .env файл в директории проекта используя в качестве шаблона .env.template

7. Запустить файл homework.py
```commandline
python homework.py
```
