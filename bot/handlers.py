from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from bot import my_bot
from logic.text_fetcher import text_divider, send_messages_to_users
from keyboard import category_callback_inline_kb, choose_callback_inline_kb, CategoryRelationCallback
import requests

dp = Dispatcher()

WEBHOOK_URL = "http://127.0.0.1:8000/api/v1"


async def handle_relation(callback_query: types.CallbackQuery, success_text: str, error_text: str, method: str):
    user_id = callback_query.from_user.id
    category = CategoryRelationCallback.unpack(callback_query.data)
    category_id = category.category_id
    previous_message = callback_query.message.text
    print(previous_message)

    try:
        response = requests.request(method, WEBHOOK_URL + f"/relation/user/{user_id}/{category_id}")
        response.raise_for_status()
        await callback_query.message.edit_text(success_text)
    except requests.exceptions.RequestException as e:
        if "Relation already exists" in str(response.text):
            await callback_query.message.edit_text("Вы уже подписаны на эту категорию. Хотите её удалить?",
                                                   reply_markup=choose_callback_inline_kb(category_id,
                                                                                          ).as_markup())
        else:
            await callback_query.message.edit_text(f"{error_text} {response.text}")


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
    response = requests.post(WEBHOOK_URL + "/user",
                             json={"tg_id": message.from_user.id, "username": message.from_user.username})
    await message.answer(response.text)


@dp.message(Command('create_relation'))
async def cmd_create_relation(message: types.Message):
    await message.answer('На какую категорию вы хотите подписаться?',
                         reply_markup=category_callback_inline_kb().as_markup())


@dp.message(Command('show_relation'))
async def cmd_get_relations(message: types.Message):
    tg_id = message.from_user.id
    response = requests.get(WEBHOOK_URL + f"/user/{tg_id}/categories")
    await message.answer(response.text)

@dp.callback_query(CategoryRelationCallback.filter(F.action == 'add'))
async def callback_relation(callback_query: types.CallbackQuery):
    await handle_relation(callback_query, "Вы успешно подписались на категорию!", "Ошибка при подписке:",
                          "POST")


@dp.callback_query(CategoryRelationCallback.filter(F.action == 'remove'))
async def callback_relation_discard(callback_query: types.CallbackQuery, ):
    await handle_relation(callback_query, "Вы успешно отписались от категории!", "Ошибка при отписке:",  #
                          "DELETE")


@dp.callback_query(CategoryRelationCallback.filter(F.action == 'category_remove_cancel'))
async def callback_relation_discard(callback_query: types.CallbackQuery):
    await cmd_create_relation(message=callback_query.message)


@dp.message((F.text.len() > 20))
async def order_fetch_handler(message: types.Message):
    users = await text_divider(message.text)
    if users:
        username_link = f'<a href="{message.from_user.url}">{message.from_user.username}</a>'
        message_text = f'Найден новый заказ от {username_link}\n{message.text}'
        await send_messages_to_users(my_bot=my_bot, users=users, message_text=message_text)
