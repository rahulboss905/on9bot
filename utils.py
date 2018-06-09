from telegram.error import TelegramError

from config import OWNER_USERNAME, OWNER_ID


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


def echo_owner_check(text):
    text = text.lower()
    assert OWNER_USERNAME.lower() not in text
    assert not ("[" in text and f"](tg://user?id={OWNER_ID})" in text)
