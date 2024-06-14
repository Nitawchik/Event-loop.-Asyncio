
#api.py



import aiohttp
import asyncio


async def fetch_character(session, url):
    async with session.get(url) as response:
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            print(f"Ошибка при получении данных с {url}")
            return None
    


async def fetch_all_characters():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1,100): #We suggest that there are nor more than 100 personages
            url = f'https://swapi.py4e.com/api/people/{i}/'
            tasks.append(fetch_character(session, url))
        return await asyncio.gather(*tasks)