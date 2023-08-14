from functions.func import connect


def main():
    count_db = 1
    k = 1

    conn, cursor = connect()

    if len(cursor.execute("PRAGMA table_info(rates)").fetchall()) > 0:
        print(f"Table was found({k}/{count_db})")
    else:
        cursor.execute("CREATE TABLE rates("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "date DATETIME,"
                       "from_currency TEXT,"
                       "to_currency TEXT,"
                       "price INTEGER)")
        print(f"Table was not found({k}/{count_db}) | Creating...")
    k += 1

    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
