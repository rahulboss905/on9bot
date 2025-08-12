import os
from typing import Iterable

# Bot configuration
BOT_TOKEN: str = os.environ["BOT_TOKEN"]
OWNER_ID: int = 7456681709  # Your user id
ADMIN_GROUP_ID: int = -1002897249216  # Admin group chat id
SPECIAL_GROUP_ID: int = -1002897249216  # Special group chat id
HEROKU_APP_NAME: str = "on9bot"  # Heroku app name (not needed for Render)

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
