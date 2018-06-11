from telegram import Bot

BOT_TOKEN = "506548905:AAFCkZ5SI9INLEb0fwRHRlEji4Or6s8B9DQ"
OWNER_ID = 463998526
ADMIN_GROUP_ID = -1001141544515
HEROKU_APP_NAME = "on9bot"

nubbot = Bot(BOT_TOKEN)

BOT = nubbot.get_me()
BOT_ID = BOT.id
BOT_NAME = BOT.first_name
BOT_USERNAME = "@" + BOT.username
BOT_LINK = f"https://t.me/{BOT.username}"

OWNER = nubbot.get_chat_member(OWNER_ID, OWNER_ID).user
OWNER_NAME = OWNER.full_name
OWNER_USERNAME = "@" + OWNER.username
OWNER_LINK = f"https://t.me/{OWNER.username}"
OWNER_MENTION = f"[{OWNER_NAME}]({OWNER_LINK})"

ADMIN_GROUP = nubbot.get_chat(ADMIN_GROUP_ID)

CAN_USE_TAG9 = (OWNER_ID, 190726372, 106665913)  # Append user ids of users to let them use /tag9.
OWNER_NICKNAMES = tuple(OWNER_NAME.lower().split()) + ("leung",)  # Append your nicknames in lowercase in the tuple.
INSULTS = ("on9", "nub", "rubbish", "trash")  # Append insults used with your names that you want your bot to respond.
