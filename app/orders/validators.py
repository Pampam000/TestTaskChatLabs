import phonenumbers

from app.config import MAX_ORDER_PRICE, MIN_ORDER_PRICE, MAX_ORDER_PRICE_STR


def check_price(price: str, min_price: int = None):
    if not price.replace(' ', '').replace('-', '').isdigit():
        raise ValueError('Укажите бюджет в правильном формате\n'
                         'Пример1: 5 000\n'
                         'Пример2: 20000')
    price = int(price)
    if price > MAX_ORDER_PRICE:
        raise ValueError(f'Максимальное значение цены: {MAX_ORDER_PRICE_STR}')

    if not min_price:
        min_price = MIN_ORDER_PRICE

    if price <= min_price:
        raise ValueError(f'Цена должна быть больше {min_price}')


def check_phone(phone: str):
    if phone.startswith('8'):
        phone = '+7' + phone[1:]
    elif phone.startswith('7'):
        phone = '+' + phone

    try:
        phone = phonenumbers.parse(phone)
    except phonenumbers.NumberParseException:
        raise ValueError('Несуществующий код страны, '
                         'введите номер ещё раз')

    if not (phonenumbers.is_valid_number(phone) and
            phonenumbers.is_possible_number(phone)):
        raise ValueError(
            'Укажите номер в правильном формате\n'
            'Пример 1: 89998887766\n'
            'Пример 2: 8-999-888-7766\n'
            'Пример 3: 8 999 888 7766\n'
            'Аналогично для номеров в международном формате(+7, +11 и т.д)')
