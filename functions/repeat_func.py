import logging

import requests
from bs4 import BeautifulSoup

import config
from loader import bot
from functions import func


async def get_rates() -> None:
    text: list[str] = list()
    text.append(get_fragment())
    text.append(get_cryptobot())
    await bot.send_message(config.chat_id, "\n".join(text))


def get_cryptobot() -> str:
    headers = {
        "Crypto-Pay-API-Token": "114575:AALg2CZcdNCQKziM4g3J9pXUBv1j8g2tdSf"
    }
    res = requests.get("https://pay.crypt.bot/api/getExchangeRates", headers=headers)
    res = res.json()
    text: list[str] = list()
    if res["ok"]:
        for currency in res["result"]:
            if currency["target"] == "RUB" and currency["source"] == "TON":
                func.new_rate("rub", "ton", round(float(currency['rate']), 2))
                text.append(f"TON: {round(float(currency['rate']), 2)}₽")
            elif currency["target"] == "RUB" and currency["source"] == "USDT":
                func.new_rate("rub", "usdt", round(float(currency['rate']), 2))
                text.append(f"USDT: {round(float(currency['rate']), 2)}₽")
            elif currency["target"] == "USD" and currency["source"] == "TON":
                func.new_rate("ton", "usdt", round(float(currency['rate']), 2))
                text.append(f"TON: {round(float(currency['rate']), 2)}$")
    if text:
        return "\n".join(text)
    logging.error(f"USDT Error\n{res}")
    return f"USDT: {res}"


def get_fragment() -> str:
    res = requests.get("https://fragment.com/numbers?filter=sale")
    prices: list[int] = list()
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.findAll("tr", {"class": "tm-row-selectable"})[:10]
        for row in rows:
            price = int(
                row.find("div", {"class": "table-cell-value tm-value icon-before icon-ton"}).text.replace(",", ""))
            prices.append(price)
    else:
        logging.error(f"Fragment Error [{res.status_code}]\n{res.text}")
        return f"Fragment: {res.status_code}"
    func.new_rate("number", "ton", min(prices))
    return f"Fragment: {min(prices)}-{max(prices)} Ton"
