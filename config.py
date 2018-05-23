from telegram import Bot

# Create a bot by talking to BotFather (t.me/BotFather).
# You are required to set a username and suggested to disable your bot's privacy mode.

# Important information
BOT_TOKEN = "506548905:AAFCkZ5SI9INLEb0fwRHRlEji4Or6s8B9DQ"  # Paste your bot token here
OWNER_ID = 463998526  # Replace with your user id.
ADMIN_GROUP_ID = -1001141544515  # Id of group/supergroup/channel to receive feedback and errors.
HEROKU_APP_NAME = "on9bot"  # Paste your Heroku app name here if you are going to host this on Heroku.


# DO NOT AMEND THE FOLLOWING EXCEPT VARIABLES IN "YOUR PREFERENCES":.

# Bot instance to retrieve (updated) information of itself and you.
bot = Bot(BOT_TOKEN)

# Bot information
BOT = bot.get_me()
BOT_ID = BOT.id
BOT_NAME = BOT.first_name
BOT_USERNAME = BOT.username
BOT_LINK = f"https://t.me/{BOT_USERNAME}"

# Owner information
OWNER = bot.get_chat_member(OWNER_ID, OWNER_ID).user
OWNER_NAME = OWNER.full_name
OWNER_USERNAME = OWNER.username
OWNER_LINK = f"https://t.me/{OWNER_USERNAME}"
OWNER_MENTION = f"[{OWNER_NAME}]({OWNER_LINK})"

# Admin group information
ADMIN_GROUP = bot.get_chat(ADMIN_GROUP_ID)

# Your preferences
CAN_USE_TAG9 = (OWNER_ID, 190726372, 106665913)  # Append user ids of users to let them use /tag9.
OWNER_NICKNAMES = tuple(OWNER_NAME.lower().split()) + ("leung",)  # Append your nicknames in lowercase in the tuple.
INSULTS = ("on9", "nub", "rubbish", "trash")  # Append insults used with your names that you want your bot to respond.
