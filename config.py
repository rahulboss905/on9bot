from telegram import Bot, User, Chat
from typing import Iterable

BOT_TOKEN: str = "506548905:AAH4PE8Fi2Fp39gBFrxkXlhVvorXPf2MLJQ"
OWNER_ID: int = 463998526
ADMIN_GROUP_ID: int = -1001141544515
SPECIAL_GROUP_ID: int = -1001295361187
HEROKU_APP_NAME: str = "on9bot"

nubbot: Bot = Bot(BOT_TOKEN)

BOT: User = nubbot.get_me()
BOT_USERNAME: str = "@" + BOT.username
BOT_LINK: str = f"https://t.me/{BOT.username}"

OWNER: User = nubbot.get_chat_member(OWNER_ID, OWNER_ID).user
OWNER_USERNAME: str = "@" + OWNER.username
OWNER_LINK: str = f"https://t.me/{OWNER.username}"
OWNER_MENTION: str = f"[{OWNER.full_name}]({OWNER_LINK})"

ADMIN_GROUP: Chat = nubbot.get_chat(ADMIN_GROUP_ID)
SPECIAL_GROUP: Chat = nubbot.get_chat(SPECIAL_GROUP_ID)

CAN_USE_TAG9: Iterable[int] = (OWNER_ID, 190726372, 106665913)  # Append user ids of users to let them use /tag9.
OWNER_NICKNAMES: Iterable[str] = tuple(OWNER.full_name.lower().split()) + ("leung",)  # Your nicknames in lowercase
INSULTS: Iterable[str] = ("on9", "nub", "rubbish", "trash")  # Append insults to respond.
