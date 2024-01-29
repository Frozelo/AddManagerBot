import asyncio
import logging
import sys
from os import getenv

from aiogram.client import bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
WEBHOOK_URL = "http://127.0.0.1:8000/api"

my_bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    from handlers import dp
    # And the run events dispatching
    await dp.start_polling(my_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
