from datetime import timedelta, datetime

from functions.func import get_date, connect
import plotly.graph_objects as go


def get_graph(_type: str, from_currency: str, to_currency: str) -> str:
    """
    Получение файла с графиком курса между двумя валютами.

    :param _type: Тип графика: 'short' для 2-х дней, 'long' для месяца.
    :param from_currency: Первая валюта.
    :param to_currency: Вторая валюта.
    :return: Путь к файлу графика в формате "перваяВалюта_втораяВалюта.png".
    """
    if _type == "long":
        return long_graph(from_currency, to_currency)
    return short_graph(from_currency, to_currency)


def short_graph(from_currency: str, to_currency: str) -> str:
    """
    Получение файла с графиком курса между двумя валютами за 2 дня.

    :param from_currency: Первая валюта.
    :param to_currency: Вторая валюта.
    :return: Путь к файлу графика в формате "перваяВалюта_втораяВалюта.png".
    """
    date = get_date() - timedelta(days=2)
    conn, cursor = connect()
    # Выбираем все записи за последние 2 дня с датой и ценой
    cursor.execute("SELECT date, price FROM rates "
                   "WHERE from_currency = ? AND to_currency = ? AND date >= ?",
                   (from_currency, to_currency, date))
    data = cursor.fetchall()
    conn.close()
    return draw_graph(data, from_currency, to_currency)


def long_graph(from_currency: str, to_currency: str) -> str:
    """
    Получение файла с графиком курса между двумя валютами за месяц.

    :param from_currency: Первая валюта.
    :param to_currency: Вторая валюта.
    :return: Путь к файлу графика в формате "перваяВалюта_втораяВалюта.png".
    """
    date = get_date() - timedelta(days=31)
    # Выбираем все записи за последний месяц с датой и ценой
    conn, cursor = connect()
    cursor.execute("SELECT date, price FROM rates "
                   "WHERE from_currency = ? AND to_currency = ? AND date >= ?",
                   (from_currency, to_currency, date))
    data = cursor.fetchall()
    conn.close()
    return draw_graph(data, from_currency, to_currency)


def draw_graph(data: list[tuple[str, int]], from_currency: str, to_currency: str) -> str:
    """
    Отрисовка графика курса обмена между двумя валютами.

    :param data: Список кортежей, где первый элемент - дата, второй - цена обмена.
    :param from_currency: Первая валюта.
    :param to_currency: Вторая валюта.
    :return: Путь к файлу графика в формате "перваяВалюта_втораяВалюта.png".
    """
    dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f") for row in data]
    prices = [row[1] for row in data]
    # Создание фигуры графика с данными
    fig = go.Figure(
        data=[
            go.Scatter(
                x=dates,
                y=prices,
                mode='lines',
                line={'color': '#ff006a'}
            ),
        ]
    )

    # Настройка параметров отображения графика
    fig.update_layout(
        title=f'{from_currency.upper()} to {to_currency.upper()}',
        xaxis_title='Date',
        yaxis_title=f'Price ({to_currency.upper()})',
        xaxis_rangeslider_visible=False
    )

    # Сохранение графика в файл
    file_name = f"{from_currency}_{to_currency}.png"
    fig.write_image(file_name, width=1024)
    return file_name
