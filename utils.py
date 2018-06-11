from telegram.ext import BaseFilter
from telegram.error import TelegramError

from config import OWNER_USERNAME, OWNER, BOT


# Constants


GITHUB_SOURCE_CODE_LINK = "https://github.com/Tr-Jono/on9bot"
MARKDOWN_ERROR_TEXT = """no u, markdown error occurred: {}.
Parse mode = Markdown. Use a backslash (\"\\\") before a markdown character to escape it, like this:
\"\_\", \"\*\", \"\`" """


# Functions


def yn_processor(expression):
    return "Yes" if expression else "No"


def del_msg(msg):
    try:
        msg.delete()
    except TelegramError:
        pass


def kick_member(chat, user_id):
    try:
        chat.kick_member(user_id)
    except TelegramError:
        pass


def echo_owner_check(text):
    text = text.lower()
    assert OWNER_USERNAME.lower() not in text
    assert not ("[" in text and f"](tg://user?id={OWNER.id})" in text)


def check_number_man(user):
    if (user.last_name and len(user.first_name) == len(user.last_name) == 8 and
            user.first_name.isdigit() and user.last_name.isdigit()):
            return True
    return False


# Custom Filters


class CheckNumberMan(BaseFilter):
    name = 'CheckNumberMan'

    def filter(self, message):
        return check_number_man(message.from_user)


class BotIsAdmin(BaseFilter):
    name = 'BotIsAdmin'

    def filter(self, message):
        admins = message.chat.get_administrators
        if BOT.id in [admin.id for admin in admins]:
            return True
        return False


check_number_man_filter = CheckNumberMan()
bot_is_admin_filter = BotIsAdmin()
