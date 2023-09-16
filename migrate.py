from functions.func import connect


def run():
    conn, cursor = connect()
    # Создание таблицы с хранением курсов валют
    cursor.execute("CREATE TABLE IF NOT EXISTS rates("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "date DATETIME,"
                   "from_currency TEXT,"
                   "to_currency TEXT,"
                   "price INTEGER)")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    run()
