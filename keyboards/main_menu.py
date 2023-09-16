from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config


def main() -> InlineKeyboardMarkup:
    """
    Главная клавиатура бота.

    :return: Клавиатура.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Number/TON", callback_data="draw_graph:number:ton"),
        InlineKeyboardButton(text="TON/USDT", callback_data="draw_graph:ton:usdt"),
        InlineKeyboardButton(text="RUB/USDT", callback_data="draw_graph:rub:usdt"),
        InlineKeyboardButton(text="RUB/TON", callback_data="draw_graph:rub:ton"),
    )
    markup.add(
        InlineKeyboardButton(text="Канал", url=config.channel_url),
    )
    return markup


def select_type_graph(from_currency: str, to_currency: str) -> InlineKeyboardMarkup:
    """
    Клавиатура выбора типа графика.

    :param from_currency: Первая валюта.
    :param to_currency: Вторая валюта.
    :return: Клавиатура.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="За 2 дня", callback_data=f"draw_graph:{from_currency}:{to_currency}:short"),
        InlineKeyboardButton(text="За месяц", callback_data=f"draw_graph:{from_currency}:{to_currency}:long"),
        InlineKeyboardButton(text="Назад", callback_data=f"draw_graph"),
    )
    return markup


def back(call_data: str) -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой назад.

    :param call_data: значение callback_data.
    :return: Клавиатура.
    """
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"{call_data}"),
    )
    return markup
