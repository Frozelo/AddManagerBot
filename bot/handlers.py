from aiogram import types, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboard import category_callback_inline_kb, choose_callback_inline_kb, CategoryRelationCallback, \
    CategoryRelationDiscardCallback

import requests

dp = Dispatcher()

WEBHOOK_URL = "http://127.0.0.1:8000/api"


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Это стартовая страница напиши /help для списка команд",
                         reply_markup=category_callback_inline_kb().as_markup())


@dp.message(Command('help'))
async def help_command_handler(message: Message):
    help_text = "Доступные команды:\n" \
                "/create_user - создать пользователя\n" \
                "/create_relation - создать отношение пользователя и категории\n" \
                "/get_users_by_category - получить список пользователей по категории"
    await message.answer(help_text)


@dp.message(Command('create_user'))
async def cmd_create_user(message: types.Message):
    response = requests.post(WEBHOOK_URL + "/create-user",
                             json={"tg_id": message.from_user.id, "username": message.from_user.username})
    await message.answer(response.text)


@dp.message(Command('create_relation'))
async def cmd_create_relation(message: types.Message):
    await message.answer('На какую категорию вы хотите подписаться?',
                         reply_markup=category_callback_inline_kb().as_markup())


@dp.callback_query(CategoryRelationCallback.filter(F.action == 'add'))
async def callback_relation(callback_query: types.CallbackQuery):
    user_id = 6
    category_id = callback_query.data

    try:
        # Ваш код для отправки запроса на создание отношения пользователя и категории
        response = requests.post(WEBHOOK_URL + "/create-user-categories-relation",
                                 json={"user_id": user_id, "category_id": category_id})
        response.raise_for_status()
        await callback_query.message.edit_text("Вы успешно подписались на категорию!")
    except requests.exceptions.RequestException as e:
        await callback_query.message.edit_text('Кажется, вы уже подписаны на этот канал. Хотите отписаться?',
                                               reply_markup=choose_callback_inline_kb().as_markup())


@dp.callback_query(CategoryRelationDiscardCallback.filter(F.action == 'delete_relation'))
async def callback_relation_delete(callback_query: types.CallbackQuery):
    await callback_query.message.answer('ok')
