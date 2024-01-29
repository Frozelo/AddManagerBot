from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CategoryRelationCallback(CallbackData, prefix="relation"):
    action: str
    category_id: int


def category_callback_inline_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="SMM",
                                   callback_data=CategoryRelationCallback(action='add', category_id=1).pack()))
    builder.add(
        types.InlineKeyboardButton(text="Контекстная реклама",
                                   callback_data=CategoryRelationCallback(action='add', category_id=2).pack()))
    builder.add(
        types.InlineKeyboardButton(text="Frontend",
                                   callback_data=CategoryRelationCallback(action='add', category_id=3).pack()))
    builder.add(
        types.InlineKeyboardButton(text="Backend",
                                   callback_data=CategoryRelationCallback(action='add', category_id=4).pack()))

    return builder


def choose_callback_inline_kb(category_id):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="Да",
                                   callback_data=CategoryRelationCallback(action='remove',
                                                                          category_id=category_id).pack()))
    builder.add(
        types.InlineKeyboardButton(text="Нет",
                                   callback_data=CategoryRelationCallback(action='category_remove_cancel',
                                                                          category_id=category_id).pack()))

    return builder
