import asyncio
import re

import requests
from aiogram import types
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
    keywords = extract_keywords(message)
    for keyword, category in keywords:
        if keyword in CATEGORIES_KEYWORDS:
            return await get_response_users(CATEGORIES_KEYWORDS[keyword])


def extract_keywords(message):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([message])
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]
    sorted_indices = tfidf_scores.argsort()[::-1]
    keywords = [(feature_names[idx], tfidf_scores[idx]) for idx in sorted_indices]
    return keywords


async def send_message_async(my_bot, user_id, text):
    try:
        await my_bot.send_message(user_id, text)
        print(f"Сообщение отправлено пользователю с ID {user_id}")
    except TelegramAPIError as e:
        print(f"Ошибка при отправке сообщения пользователю с ID {user_id}: {e}")


async def send_messages_to_users(my_bot, users, message_text):
    tasks = []
    for user in users:
        task = send_message_async(my_bot, user['tg_id'], message_text)
        tasks.append(task)

    await asyncio.gather(*tasks)


