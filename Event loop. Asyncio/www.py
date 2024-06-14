#main.py

import sqlite3
import db, api
import asyncio
import json


def insert_character(conn, character):
    cursor = conn.cursor()

    # Проверяем наличие всех необходимых ключей и присваиваем им пустое значение, если они отсутствуют
    required_keys = ['birth_year', 'eye_color', 'films', 'gender', 'hair_color', 'height', 'homeworld', 'mass', 'name', 'skin_color', 'species', 'starships', 'vehicles', 'created', 'edited', 'url']
    for key in required_keys:
        if key not in character:
            character[key] = ''

    # Используем автоинкрементное поле id
    cursor.execute('''
        INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles, created, edited, url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (character['birth_year'], character['eye_color'], ', '.join(character['films']), character['gender'], character['hair_color'], character['height'], character['homeworld'], character['mass'], character['name'], character['skin_color'], ', '.join(character['species']), ', '.join(character['starships']), ', '.join(character['vehicles']), character['created'], character['edited'], character['url']))

    # Получаем последний автоматически сгенерированный первичный ключ
    character['id'] = cursor.lastrowid

   # Выводим данные персонажа в консоль
    print(f"Персонаж {character['name']} успешно добавлен в базу данных с id {character['id']}.")

        # Выводим данные персонажа в формате JSON в одну строку в консоль
    print(json.dumps(character, separators=(',', ':'), ensure_ascii=False))

    conn.commit()

async def main():
    db.create_db()
    print("База данных успешно создана.")
    conn = sqlite3.connect('starwars.db')

    try:
        characters = await api.fetch_all_characters()
        print(f"Получено {len(characters)} персонажей.")
              
        # Проверяем, есть ли исключения в результатах
        for result in characters:
            if isinstance(result, Exception):
                print(f"Произошла ошибка при получении данных: {result}")
                continue
            insert_character(conn, result)
    except Exception as e:
        print(f"Произошла ошибка при получении или вставке данных: {e}")
    finally:
        conn.close()
        print("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    asyncio.run(main())