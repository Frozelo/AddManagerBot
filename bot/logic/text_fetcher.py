import asyncio

import numpy as np

from aiogram.client.session import aiohttp
from aiogram.exceptions import TelegramAPIError

from sklearn.feature_extraction.text import TfidfVectorizer

CATEGORIES_KEYWORDS = {
    'smm': 1,
    'cмм': 1,
    'смм': 1,
    'context': 2,
    'контекстная реклама': 2,
    'контекст': 2,
    'frontend': 3,
    'front-end': 3,
    'фронтенд': 3,
    'фронт': 3,
    'backend': 4,
    'back-end': 4,
    'бэкенд': 4,
    'бэк': 4,
}

WEBHOOK_URL = "http://127.0.0.1:8000/api/v1"


async def get_response_users(category_id):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(WEBHOOK_URL + f"/category/{category_id}") as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Ошибка при отправке запроса: {e}")


async def text_divider(message: str):
    message_lower = message.lower()
    for keyword, category in CATEGORIES_KEYWORDS.items():
        if keyword in message_lower:
            return await get_response_users(category)


async def send_message_to_user(my_bot, user_id, message_text):
    try:
        await my_bot.send_message(user_id, message_text)
        print(f"Сообщение отправлено пользователю с ID {user_id}")
    except TelegramAPIError as e:
        print(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")


async def send_messages_to_users(my_bot, users, message_text):
    tasks = []
    for user in users:
        task = send_message_to_user(my_bot, user['tg_id'], message_text)
        tasks.append(task)
    await asyncio.gather(*tasks)
