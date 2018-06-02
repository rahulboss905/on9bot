from telegram import Bot

#################################################   #################################################
################ SUPER IMPORTANT ################   ################ SUPER IMPORTANT ################
#################################################   #################################################
###>>>>> RENAME THIS FILE TO "config.py" <<<<<###   ###>>>>> RENAME THIS FILE TO "config.py" <<<<<###
#################################################   #################################################
#################################################   #################################################

# Create a bot by talking to BotFather (t.me/BotFather).
# You are required to set a username and suggested to disable your bot's privacy mode.

# IMPORTANT INFORMATION
BOT_TOKEN = ""  # Paste your bot token here
OWNER_ID = 123456789  # Replace with your user id.
ADMIN_GROUP_ID = -1001234512345  # Id of group/supergroup/channel to receive feedback and errors.
HEROKU_APP_NAME = ""  # Paste your Heroku app name here if you are going to host this on Heroku.


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
OWNER_USERNAME = "@" + OWNER.username
OWNER_LINK = f"https://t.me/{OWNER.username}"
OWNER_MENTION = f"[{OWNER_NAME}]({OWNER_LINK})"

# Admin group information
ADMIN_GROUP = bot.get_chat(ADMIN_GROUP_ID)

# Your preferences                                                                    | | | | |
CAN_USE_TAG9 = (OWNER_ID,)  # Append user ids of users to let them use /tag9.        \/\/\/\/\/
OWNER_NICKNAMES = tuple(OWNER_NAME.lower().split()) + ()  # Append your nicknames in LOWERCASE in the empty tuple.
INSULTS = ("on9", "nub", "rubbish", "trash")  # Append insults used with your names that you want your bot to respond.


# Running locally (YOU MUST MAKE SURE YOU ARE RUNNING Python 3.6+, I USE F-STRINGS):
# You only need to copy the three .py files in the repo to the folder.
# Run "pip install python-telegram-bot" and append with "--upgrade" if you haven't updated. Ignore if ptb** is updated.
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

# **ptb stands for python-telegram-bot if you don't know


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

# *From now on, you have two run these two commands when you push changes.
