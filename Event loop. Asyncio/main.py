#main.py


import sqlite3
import db, api
import asyncio
import json
import aiohttp
import aiosqlite

from api import fetch_character, fetch_all_characters

# Функция для получения названий из URL (не используется в текущем коде)
async def get_names_from_urls(session, urls):
    names = []
    for url in urls:
        async with session.get(url) as resp:
            data = await resp.json()
            names.append(data['title'])
    return names

# Функция для проверки существования персонажа в базе данных
async def character_exists(conn, name):
    async with conn.execute('SELECT 1 FROM characters WHERE name=?', (name,)) as cursor:
        return await cursor.fetchone() is not None
    

    

async def insert_character(conn, character):
    try:
        name_key = 'name'
        if name_key in character:
            name = character[name_key]
            if not await character_exists(conn, name):
                # Получаем список фильмов персонажа, если они есть
                film_urls = character.get('films', [])
                # Получаем список видов персонажа, если они есть
                species_urls = character.get('species', [])
                # Получаем список кораблей персонажа, если они есть
                starship_urls = character.get('starships', [])
                # Получаем список транспорта персонажа, если они есть
                vehicle_urls = character.get('vehicles', [])

                # Преобразуем URL-адреса в строки, если это необходимо
                film_urls = [str(url) for url in film_urls]
                species_urls = [str(url) for url in species_urls]
                starship_urls = [str(url) for url in starship_urls]
                vehicle_urls = [str(url) for url in vehicle_urls]

                # Получаем данные о фильмах, видах, кораблях и транспорте
                async with aiohttp.ClientSession() as session:
                    film_data = await fetch_character(session, film_urls[0]) if film_urls else {}
                    species_data = await fetch_character(session, species_urls[0]) if species_urls else {}
                    starship_data = await fetch_character(session, starship_urls[0]) if starship_urls else {}
                    vehicle_data = await fetch_character(session, vehicle_urls[0]) if vehicle_urls else {}

                # Обновляем персонажей с данными о фильмах, видах, кораблях и транспорте
                character['films'] = film_data.get('title', '') if film_data else ''
                character['species'] = species_data.get('title', '') if species_data else ''
                character['starships'] = starship_data.get('title', '') if starship_data else ''
                character['vehicles'] = vehicle_data.get('title', '') if vehicle_data else ''

                # Вставляем персонажа в базу данных
                await conn.execute('''
                    INSERT INTO characters (birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles, created, edited, url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (character.get('birth_year'), character.get('eye_color'), character['films'], character.get('gender'), character.get('hair_color'), character.get('height'), character.get('homeworld'), character.get('mass'), character['name'], character.get('skin_color'), character['species'], character['starships'], character['vehicles'], character.get('created'), character.get('edited'), character.get('url')))
                await conn.commit()  # Не забываем коммитить изменения
                print(f"Персонаж {character['name']} успешно добавлен в базу данных.")
            else:
                print(f"Персонаж {character['name']} уже существует в базе данных.")
        else:
            print(f"Персонаж без имени: {character}")
    except Exception as e:
        print(f"Произошла ошибка при получении или вставке данных для персонажа {character.get('name', 'без имени')}: {e}")
        # Продолжаем работу, не прерывая ее



# Пример использования функции insert_character в цикле
async def process_characters(characters):
    async with aiosqlite.connect('starwars.db') as conn:
        for character in characters:
            if isinstance(character, dict) and 'name' in character:
                try:
                    await insert_character(conn, character)
                except Exception as e:
                    print(f"Произошла ошибка при обработке персонажа {character['name']}: {e}")
                    # Продолжаем работу, не прерывая ее
            else:
                print(f"Некорректный персонаж: {character}")



# Главная асинхронная функция, которая управляет выполнением всего кода
async def main():
    characters = await fetch_all_characters()  # Этот вызов является асинхронным

    # Распечатать список персонажей для проверки на дубликаты
    for character in characters:
        print(character)

    db.create_db()  # Этот вызов синхронной функции
    print("База данных успешно создана.")

    # Вставляем персонажей в базу данных
    # Этот блок кода также выполняется асинхронно
    async with aiosqlite.connect('starwars.db') as conn:
        try:
            await process_characters(characters)
        except Exception as e:
            print(f"Произошла ошибка при получении или вставке данных: {e}")
    print("Соединение с базой данных закрыто.")

# Точка входа в программу, которая запускает асинхронный цикл событий
if __name__ == '__main__':
    asyncio.run(main())