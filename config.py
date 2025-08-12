import os
from typing import Iterable

# Bot configuration
BOT_TOKEN: str = os.environ["BOT_TOKEN"]
OWNER_ID: int = 7456681709  # Your user id
ADMIN_GROUP_ID: int = -1002897249216  # Admin group chat id
SPECIAL_GROUP_ID: int = -1002897249216  # Special group chat id
HEROKU_APP_NAME: str = "on9bot"  # Heroku app name

# Users who can use /tag9 command
CAN_USE_TAG9: Iterable[int] = (OWNER_ID, 190726372, 106665913, 537248339, 540933895, 401742123)

# GitHub source code link
GITHUB_SOURCE_CODE_LINK: str = "https://github.com/your-repo"

# Markdown error text
MARKDOWN_ERROR_TEXT: str = "Error formatting text: {}\nMake sure you're using valid Markdown syntax."

# Bot username (will be set asynchronously in main)
BOT_USERNAME: str = None

# Owner information
OWNER_USERNAME: str = "your_username"  # Replace with your Telegram username without '@'
OWNER_MENTION: str = f"[Your Name](https://t.me/{OWNER_USERNAME})"  # Replace "Your Name" with your actual name

# Running locally:
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


# Deploying to Render/Heroku
# You will need to copy all the files (excluding trash.py, README.md and LICENSE.md) in the repo to a folder.
# Fill in the required information in config.py.
# Create an account on Render/Heroku.
# Download Heroku CLI if using Heroku: https://devcenter.heroku.com/articles/getting-started-with-python#set-up
# For Render, create a new Web Service and connect your repository
# Add all required environment variables in your deployment environment:
#   BOT_TOKEN, OWNER_ID, ADMIN_GROUP_ID, SPECIAL_GROUP_ID, HEROKU_APP_NAME, etc.
