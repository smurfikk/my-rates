import logging

import requests
from bs4 import BeautifulSoup

import config
from loader import bot
from functions import func


async def get_rates() -> None:
    """
    Получает курсы криптовалют, сохраняет их и отправляет собранную информацию в канал.
    """
    text: list[str] = list()
    text.append(get_fragment())
    text.append(get_cryptobot())
    await bot.send_message(config.chat_id, "\n".join(text))


def get_cryptobot() -> str:
    """
    Получение курсов криптовалют из @CryptoBot.

    :return: Строка с текущими курсами криптовалют в формате: "ВАЛЮТА1: КУРС ВАЛЮТА2".
    """
    headers = {
        "Crypto-Pay-API-Token": config.cryptobot_token
    }
    res = requests.get("https://pay.crypt.bot/api/getExchangeRates", headers=headers)
    res = res.json()
    text: list[str] = list()
    if res["ok"]:
        # Извлечение и сохранение курсов для целевых валютных пар
        for currency in res["result"]:
            if currency["target"] == "RUB" and currency["source"] == "TON":
                rate = round(float(currency["rate"]), 2)
                func.new_rate("rub", "ton", rate)
                text.append(f"TON: {rate}₽")
            elif currency["target"] == "RUB" and currency["source"] == "USDT":
                rate = round(float(currency["rate"]), 2)
                func.new_rate("rub", "usdt", rate)
                text.append(f"USDT: {rate}₽")
            elif currency["target"] == "USD" and currency["source"] == "TON":
                rate = round(float(currency["rate"]), 2)
                func.new_rate("ton", "usdt", rate)
                text.append(f"TON: {rate}$")
    if text:
        # Компиляция результатов в одну строку
        return "\n".join(text)
    # Логирование ошибки при отсутствии ожидаемых результатов
    logging.error(f"USDT Error\n{res}")
    return f"USDT: {res}"


def get_fragment() -> str:
    """
    Получение цен на номера с сайта fragment.com.

    :return: Строка с минимальной и максимальной ценой из последних 10 номеров.
    """
    res = requests.get("https://fragment.com/numbers?filter=sale")
    prices: list[int] = list()

    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        # Извлекаем данные по ценам из последних 10 записей на сайте
        rows = soup.findAll("tr", {"class": "tm-row-selectable"})[:10]
        for row in rows:
            # Преобразование текстовой цены в целое число
            price = int(
                row.find("div", {"class": "table-cell-value tm-value icon-before icon-ton"}).text.replace(",", ""))
            prices.append(price)
    else:
        # Логирование ошибки, если не удалось получить данные с сайта
        logging.error(f"Fragment Error [{res.status_code}]\n{res.text}")
        return f"Fragment: {res.status_code}"
    # Запись минимальной цены в базу данных
    func.new_rate("number", "ton", min(prices))
    return f"Fragment: {min(prices)}-{max(prices)} Ton"
