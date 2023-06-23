import os

import dotenv

dotenv.load_dotenv()

# Bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
SEND_REQUEST_BUTTON = 'Оставить заявку'
BUY_PRODUCT_BUTTON = 'Купить товар'
MY_BALANCE_BUTTON = 'Мой баланс'
MAIN_BUTTONS = [SEND_REQUEST_BUTTON, BUY_PRODUCT_BUTTON, MY_BALANCE_BUTTON]
SEND_MESSAGE_BUTTON = 'Отправить сообщение пользователям'
ADMIN_BUTTONS = [SEND_MESSAGE_BUTTON]

# Payment
U_KASSA_TOKEN = os.getenv('U_KASSA_TOKEN')
PAYMENT_INLINE_BUTTONS = ['Купить 1 раз', 'Купить 2 раза']
PRODUCT_NAME = 'Условная единица'
PRODUCT_DESCRIPTION = 'Покупка условной единицы'
PRODUCT_PAYLOAD = 'payload'
PRODUCT_CURRENCY = 'rub'
PRODUCT_PRICE = 10000  # 100 rub

# Db
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

# Orders
MIN_ORDER_PRICE = 0
MAX_ORDER_PRICE = 1000000  # 1 million
MAX_ORDER_PRICE_STR = '1 000 000 (1 миллион)'
TIME_BEFORE_ORDER_NOTIFICATION_IN_SECONDS = 600  # 10 minutes

# Hello messages
HELLO_MESSAGE = """
* Привет! Я бот для оставления заявок на создание чат-ботов. Вот что я умею: *

_Команды_:
    /start /help - Получить это сообщение и выйти в главное меню\n

_Главное меню_:
    "Оставить заявку" - Следуя инструкциям бота, вы можете оставить заявку на создание чат-бота для вашего бизнеса\n
    "Купить товар" - Вы можете приобрети 'Условную единицу' за 100₽ или 2 за 200₽\n
    "Мой баланс" - Вы можете посмотреть ваш баланс в у.е.\n
"""

ADMIN_HELLO_MESSAGE = """
_Админка_:
    "Отправить сообщение пользователям" - Создать рассылку (функции админки видят только администарторы)
"""
