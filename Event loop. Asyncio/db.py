#db.py


import sqlite3


def create_db():
    conn = sqlite3.connect('starwars.db')
    cursor = conn.cursor()


   # Проверяем, существует ли таблица
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='characters'")
    if not cursor.fetchone():
        # Если таблицы нет, создаем ее
        cursor.execute('''
            CREATE TABLE characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                birth_year TEXT,
                eye_color TEXT,
                films TEXT,
                gender TEXT,
                hair_color TEXT,
                height TEXT,
                homeworld TEXT,
                mass TEXT,
                name TEXT,
                skin_color TEXT,
                species TEXT,
                starships TEXT,
                vehicles TEXT,
                created TEXT,
                edited TEXT,
                url TEXT
            )
        ''')



    conn.commit()
    conn.close()