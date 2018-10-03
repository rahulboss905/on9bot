import os  # remove this import and change BOT_TOKEN below to your bot token
from typing import Iterable

from telegram import Bot, User, Chat

# Create a bot by talking to BotFather (t.me/BotFather).
# You are required to set a username and suggested to disable your bot's privacy mode.

# Replace all of these constants
BOT_TOKEN: str = os.environ["BOT_TOKEN"]  # Replace with bot token. Delete this env var thing and remove os import
OWNER_ID: int = 463998526  # Your user id
ADMIN_GROUP_ID: int = -1001141544515  # Admin group chat id
SPECIAL_GROUP_ID: int = -1001295361187  # Special group chat id
HEROKU_APP_NAME: str = "on9bot"  # Heroku app name

#                              C A N  U S E  F O R E V E R
CAN_USE_TAG9: Iterable[int] = (OWNER_ID, 190726372, 106665913, 537248339, 540933895, 401742123)

# Do not modify these
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

# Running locally (YOU MUST MAKE SURE YOU ARE RUNNING Python 3.6+, I USE F-STRINGS):
# You only need to copy the .py files (excluding trash.py) from the repo to a folder.
# Run "pip install python-telegram-bot" if you haven't. Remember to update it.
# Fill in the required information in config.py.
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
# You will need to copy all the files (excluding trash.py, README.md and LICENSE.md) in the repo to a folder.
# Fill in the required information in config.py.
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
