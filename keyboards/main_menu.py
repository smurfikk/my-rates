from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config


def main():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Numbers/TON", callback_data="draw_graph:numbers:ton"),
        InlineKeyboardButton(text="TON/USDT", callback_data="draw_graph:ton:usdt"),
        InlineKeyboardButton(text="USDT/RUB", callback_data="draw_graph:usdt:rub"),
        InlineKeyboardButton(text="TON/RUB", callback_data="draw_graph:ton:rub"),
    )
    markup.add(
        InlineKeyboardButton(text="Канал", url=config.channel_url),
    )
    return markup


def select_type_graph(from_currency: str, to_currency: str):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="За 2 дня", callback_data=f"draw_graph:{from_currency}:{to_currency}:short"),
        InlineKeyboardButton(text="За месяц", cafllfback_data=f"draw_graph:{from_currency}:{to_currency}:long"),
    )
    return markup


def back(call_data: str):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Назад", callback_data=f"{call_data}"),
    )
    return markup
