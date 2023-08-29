from datetime import timedelta, datetime

from functions.func import get_date, connect
import matplotlib.pyplot as plt


def get_graph(_type: str, from_currency: str, to_currency: str) -> str:
    if _type == "long":
        return long_graph(from_currency, to_currency)
    return short_graph(from_currency, to_currency)


def short_graph(from_currency: str, to_currency: str) -> str:
    date = get_date() - timedelta(days=2)
    conn, cursor = connect()
    cursor.execute("SELECT strftime('%Y-%m-%d %H:00:00', date) AS hour, AVG(price) FROM rates "
                   "WHERE from_currency = ? AND to_currency = ? AND date >= ? GROUP BY hour",
                   (from_currency, to_currency, date))
    data = cursor.fetchall()
    conn.close()
    return draw_graph(data, from_currency, to_currency)


def long_graph(from_currency: str, to_currency: str) -> str:
    date = get_date() - timedelta(days=31)
    conn, cursor = connect()
    cursor.execute("SELECT strftime('%Y-%m-%d 00:00:00', date) AS hour, AVG(price) FROM rates "
                   "WHERE from_currency = ? AND to_currency = ? AND date >= ? GROUP BY hour",
                   (from_currency, to_currency, date))
    data = cursor.fetchall()
    conn.close()
    return draw_graph(data, from_currency, to_currency)


def draw_graph(data: list[tuple], from_currency: str, to_currency: str) -> str:
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S").strftime("%d %b %H:%M") for row in data]
    prices = [row[1] for row in data]
    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, marker=".")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.title(f"Изменение курса обмена {from_currency.upper()} на {to_currency.upper()}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if len(dates) > 30:
        plt.xticks(dates[::2])
    plt.grid(True)
    file_name = f"{from_currency}_{to_currency}.png"
    plt.savefig(file_name)
    return file_name
