from telegram import Bot, User, Chat
from typing import Iterable

#################################################   #################################################
################ SUPER IMPORTANT ################   ################ SUPER IMPORTANT ################
#################################################   #################################################
###>>>>> RENAME THIS FILE TO "config.py" <<<<<###   ###>>>>> RENAME THIS FILE TO "config.py" <<<<<###
#################################################   #################################################
#################################################   #################################################

# Create a bot by talking to BotFather (t.me/BotFather).
# You are required to set a username and suggested to disable your bot's privacy mode.

# Fill in these required information
BOT_TOKEN: str = ""
OWNER_ID: int = 0
ADMIN_GROUP_ID: int = 0
SPECIAL_GROUP_ID: int = 0
HEROKU_APP_NAME: str = ""

# Don't modify
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

# Fill in your preferences
CAN_USE_TAG9: Iterable[int] = (OWNER_ID,)  # Append user ids of users to let them use /tag9.
OWNER_NICKNAMES: Iterable[str] = tuple(OWNER.full_name.lower().split()) + ()  # Your nicknames in LOWERCASE
INSULTS: Iterable[str] = ("on9", "nub", "rubbish", "trash")  # Append insults to respond.


# Running locally (YOU MUST MAKE SURE YOU ARE RUNNING Python 3.6+, I USE F-STRINGS):
# You only need to copy the three .py files in the repo to the folder.
# Run "pip install python-telegram-bot" if you haven't. Remember to update it.
# Rename blank_config.py to config.py and fill in the required information.
# Add a environmental variable with the name "debug" and value "yes".*
# Running the bot in PyCharm: Open On9bot.py, scroll to the bottom and press the run button on the left.
# Running the bot in cmd: cd to folder containing On9bot.py and run "python3 On9bot.py". Use Ctrl+C to stop the bot.

# *Adding environmental variables in PyCharm (If you are going to run the bot in PyCharm):
# You may go to the right top corner of the editor and press the leftmost button with a scroll down menu.
# Select Edit Configurations and you should be at the "Configuration" tab.
# Under the "Environment" section, click the "..." button besides the "Environmental variables" line.
# Select the "+" sign, type "debug" on the left and "yes" on the right.
# Press OK to close the window, then press Apply.
# You have added the environmental variable and make sure to run the code in PyCharm as well.


# Deploying to Heroku
# You will need to copy all the files in the repo to a folder.
# Rename blank_config.py to config.py and fill in the required information.
# Create an account on Heroku.
# Download Heroku on https://devcenter.heroku.com/articles/getting-started-with-python#set-up so you can run it on cmd.
# Cd to the folder containing the On9bot files (run "cd {directory name}" in cmd)
# Run the following commands:

# heroku create (run "heroku create appname" if you would like to specify a name, else a random one will be given)
# git init
# heroku git:remote -a {your heroku app name}
# git add .
# git commit -am "{commit message}"*
# git push heroku master*

# *From now on, you have to run these two commands when you push changes.
