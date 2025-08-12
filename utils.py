import re
from typing import Union

from telegram import User, Chat, Message, ChatMember
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
        await chat.ban_member(user_id)
    except TelegramError:
        pass

def echo_owner_check(text: str) -> None:
    text = text.lower()
    assert OWNER_USERNAME.lower() not in text
    assert not ("[" in text and f"](tg://user?id={OWNER_ID})" in text)

def check_number_man(user: User) -> bool:
    return bool(re.match(r"(\d{8}) \1", user.full_name))


# Custom filter classes
class CheckNumberManFilter(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        return check_number_man(message.from_user)

class BotIsAdminFilter(filters.MessageFilter):
    def __init__(self):
        super().__init__()

    async def check_admin(self, chat: Chat, bot_id: int) -> bool:
        try:
            admins = await chat.get_administrators()
            return any(admin.user.id == bot_id for admin in admins)
        except TelegramError:
            return False

    async def filter(self, message: Message) -> bool:
        return await self.check_admin(message.chat, message.bot.id)


# Create filter instances
check_number_man_filter = CheckNumberManFilter()
bot_is_admin_filter = BotIsAdminFilter()
