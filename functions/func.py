from datetime import datetime
import sqlite3
import pytz


def connect(_dict: bool = False):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    if _dict:
        cursor.row_factory = dict_factory
    return conn, cursor


def dict_factory(cursor, row):
    save_dict = {}
    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]
    return save_dict


def get_date():
    date = datetime.now(pytz.timezone("Europe/Moscow")).replace(tzinfo=None)
    return date


def new_rate(from_currency: str, to_currency: str, price: int | float):
    conn, cursor = connect()
    cursor.execute("INSERT INTO rates (date, from_currency, to_currency, price) VALUES (?, ?, ?, ?)",
                   [get_date(), from_currency, to_currency, price])
    conn.commit()
    conn.close()
