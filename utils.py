import re
from typing import Union

from telegram import User, Chat, Message
from telegram.error import TelegramError
from telegram.ext import filters
from config import OWNER_USERNAME, OWNER_ID

# Constants
POKER_CARDS = [f"{f}{c}" for f in ("♦️", "♣️", "♥️", "♠️") for c in (*"A23456789", "10", *"JQK")]
GITHUB_SOURCE_CODE_LINK = "https://github.com/Tr-Jono/on9bot"
RAND_FUNC_POST_LINK = ""
MARKDOWN_ERROR_TEXT = r'''Markdown error occurred: {}.
Parse mode = Markdown. Use a backslash ("\") before a markdown character to escape it, like this:
"\_", "\*", "\`"'''


# Functions
def yn_processor(xpr: bool) -> str:
    return "Yes" if xpr else "No"

async def del_msg(msg: Message) -> None:
    try:
        await msg.delete()
    except TelegramError:
        pass

async def kick_member(chat: Chat, user_id: int) -> None:
    try:
        await chat.kick_member(user_id)
    except TelegramError:
        pass

def echo_owner_check(text: str) -> None:
    text = text.lower()
    assert OWNER_USERNAME.lower() not in text
    assert not ("[" in text and f"](tg://user?id={OWNER_ID})" in text)

def check_number_man(user: User) -> bool:
    return bool(re.match(r"(\d{8}) \1", user.full_name))


# Filter factories
def create_check_number_man_filter() -> filters.BaseFilter:
    return filters.create(
        lambda _, message: check_number_man(message.from_user)
    )

def create_bot_is_admin_filter() -> filters.BaseFilter:
    return filters.create(
        lambda _, message: message.bot.id in [
            admin.user.id for admin in message.chat.get_administrators()
        ]
    )


# Create filter instances
check_number_man_filter: filters.BaseFilter = create_check_number_man_filter()
bot_is_admin_filter: filters.BaseFilter = create_bot_is_admin_filter()
