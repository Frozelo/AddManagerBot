import re

import requests
from aiogram import types
from aiogram.client import bot
from aiogram.client.session import aiohttp

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

WEBHOOK_URL = "http://127.0.0.1:8000/api"


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


# async def send_messages_to_users(users, from_user, message_date, message_id, message_text):
#     messages_to_send = []
#
#     for user in users:
#         try:
#             message = types.Message(
#                 chat=types.Chat(id=user['tg_id'], type='private'),
#                 from_user=from_user,
#                 date=message_date,
#                 message_id=message_id,
#                 text=message_text
#             )
#             messages_to_send.append(message)
#         except Exception as e:
#             print(f"Ошибка при создании сообщения для пользователя с ID {user['tg_id']}: {e}")
#
#     if messages_to_send:
#         await bot.SendMessage(messages_to_send)
