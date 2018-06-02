import os
import logging
from time import sleep

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import TelegramError, TimedOut
from telegram.parsemode import ParseMode
from telegram.utils.helpers import escape_markdown

from config import *
from utils import *


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Check if given information is valid
assert type(BOT_TOKEN) == str and BOT_TOKEN != "", "Provide a valid bot token!"
assert type(OWNER_ID) == int and OWNER_ID > 0, "Provide a valid user id!"
assert OWNER_USERNAME, "Set a username! Go to Settings > Username to do so."
assert type(ADMIN_GROUP_ID) == int and ADMIN_GROUP_ID < 0, "Set a group, supergroup or channel as the admin group!"
assert type(HEROKU_APP_NAME) == str, "Your Heroku app name must be a string!"
for user_id in CAN_USE_TAG9:
    assert type(user_id) == int and user_id > 0, "You can only append CAN_USE_TAG9 with valid user ids!"
for name in OWNER_NICKNAMES:
    assert type(name) == str and name != "", "You can only append OWNER_NICKNAMES with non-empty strings!"
for insult in INSULTS:
    assert type(insult) == str and insult != "", "You can only append INSULTS with non-empty strings!"


def start(bot, update):
    update.message.reply_text(f"Use /help to see my functions. Contact {OWNER_MENTION} if you have questions, "
                              "suggestions or found a typo or error.")


def bot_help(bot, update):
    msg = update.message
    if msg.chat_id > 0:
        update.message.reply_markdown(f"Look at the code [here]({GITHUB_SOURCE_CODE_LINK}) to learn how I work, lol")


@run_async
def tag9js(bot, update):
    msg = update.message
    chat = msg.chat
    if chat.id == -1001295361187 or msg.from_user.id == OWNER_ID:
        chat.send_action("typing")
        js_info = chat.get_member(190726372)
        if js_info.user.username:
            username = "@" + js_info.user.username
            try:
                text = msg.text.split(maxsplit=1)[1]
                if "@" in text:
                    raise IndexError
                assert "{username}" in text
                text = text.replace("{username}", username)
            except IndexError:
                text = username
            except AssertionError:
                text = f"{msg.text.split(maxsplit=1)[1]} {username}"
            sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard or /remove_keyboard2 to remove the reply "
                                  "keyboard.", reply_markup=ReplyKeyboardMarkup([[text]]), quote=True)
            sleep(15)
            msg.reply_text("Tag9js over, removing reply keyboard and deleting message if no one did so...",
                           reply_markup=ReplyKeyboardRemove(), quote=False)
            del_msg(sent)
        else:
            msg.reply_text("no u, JS removed username.")
    elif chat.id < 0:
        msg.reply_text("no u")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join HK Duker", url="https://t.me/hkduker")]])
        msg.reply_text("This command can only be used in HK Duker. Click the following button join the group and try "
                       "out the command.", reply_markup=reply_markup)


def tag9(bot, update, args):
    msg = update.message
    chat = msg.chat
    chat.send_action("typing")
    if msg.from_user.id not in CAN_USE_TAG9 or msg.chat_id > 0:
        msg.reply_text("no u")
    elif msg.reply_to_message:
        tag9_part2(msg, chat.get_member(msg.reply_to_message.from_user.id))
    elif not args:
        msg.reply_text("Please reply to a user's message or provide a valid user id as an argument.")
    else:
        try:
            user_id = int(args[0])
            assert user_id > 0
            tag9_part2(msg, chat.get_member(user_id))
        except (ValueError, AssertionError):
            msg.reply_text("no u, user ids only.")
        except TimedOut:
            pass
        except TelegramError:
            msg.reply_text("no u, give a valid user id.")


@run_async
def tag9_part2(msg, u_info):
    if u_info.status in ("restricted", "left", "kicked"):
        msg.reply_text("no u, not in group or restricted")
    elif u_info.user.id in (OWNER_ID, BOT_ID):
        msg.reply_text("no u")
    elif u_info.user.is_bot:
        msg.reply_text("no u, don't tag other bots.")
    elif u_info.user.username is None:
        msg.reply_text("no u, user has no username.")
    else:
        sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard or /remove_keyboard2 to remove the reply "
                              "keyboard.", reply_markup=ReplyKeyboardMarkup([[u_info.user.name]]))
        sleep(15)
        msg.reply_text("Tag9 over, removing reply keyboard and deleting message if no one did so...",
                       reply_markup=ReplyKeyboardRemove(), quote=False)
        del_msg(sent)


def remove_keyboard(bot, update):
    msg = update.message
    if msg.chat_id < 0:
        msg.reply_text("Removing reply keyboard if there was an existing reply keyboard...",
                       reply_markup=ReplyKeyboardRemove(), quote=False)
    else:
        msg.reply_text("no u")


def remove_keyboard2(bot, update):
    msg = update.message
    if msg.chat_id > 0:
        msg.reply_text("no u")
        return
    sent = msg.reply_text("Replacing reply keyboard if there was an existing reply keyboard...",
                          reply_markup=ReplyKeyboardMarkup([["I AM A STUPID ANIMAL THAT LIKES TO CLICK REPLY KEYBOARD "
                                                             "BUTTONS"]]), quote=False)
    del_msg(sent)
    msg.reply_text("Removing reply keyboard...", reply_markup=ReplyKeyboardRemove(), quote=False)


def echo(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    try:
        text = msg.text_markdown_urled.split(maxsplit=1)[1]
        try:
            echo_owner_check(text)
            if rmsg:  # if message has args and replies to another message
                rmsg.reply_markdown(text, disable_web_page_preview=True)
            else:  # if message has args but does not reply to another message
                msg.reply_markdown(text, disable_web_page_preview=True, quote=False)
        except AssertionError:
            msg.reply_text("Tag your mother?!")
        except TimedOut:
            pass
        except TelegramError as e:
            msg.reply_text(MARKDOWN_ERROR_TEXT.format(str(e)))
        else:
            del_msg(msg)
    except IndexError:
        if not rmsg:  # if message has no arguments and does not reply to another message
            msg.reply_markdown("no u, use `/r [text]` or reply to a message (or both).")
        elif not rmsg.text:  # if message has no arguments and replied message does not have text
            msg.reply_text("no u, messages with text only.")
        else:  # if message has no arguments and replies to a message with text
            text = rmsg.text_markdown_urled
            try:
                echo_owner_check(text)
                msg.reply_markdown(text, disable_web_page_preview=True, quote=False)
            except AssertionError:
                msg.reply_text("Tag your mother?!")
            except TimedOut:
                pass
            except TelegramError as e:
                msg.reply_text(MARKDOWN_ERROR_TEXT.format(str(e)))
            else:
                del_msg(msg)


def user_info(bot, update):
    msg = update.message
    if msg.chat_id > 0:
        msg.reply_text("no u, groups only.")
        return
    if not msg.reply_to_message:
        msg.reply_text("no u, reply to a message.")
        return
    chat = msg.chat
    chat.send_action("typing")
    user = msg.reply_to_message.from_user
    title = escape_markdown(chat.title)
    text = "*Information of this bot*" if user.is_bot else "*Information of this user*"
    text += f"\n\nUser id: `{user.id}`\nName: {escape_markdown(user.full_name)}"
    if user.username:
        text += f"\nUsername: @{escape_markdown(user.username)}"
    if user.language_code:
        text += f"\nLanguage code: {user.language_code}"
    try:
        nub = chat.get_member(user.id)
        s = nub.status
    except TelegramError:
        msg.reply_text(text)
        return
    if s == "creator":
        text += f"\n\n*Creator* of {title}"
    elif s == "administrator":
        text += f"\n\n*Administrator* of {title}"
        text += f"\nCan change group info: {yn_processor(nub.can_change_info)}"
        text += f"\nCan delete messages: {yn_processor(nub.can_delete_messages)}"
        text += f"\nCan restrict, ban and unban members: {yn_processor(nub.can_restrict_members)}"
        text += f"\nCan pin messages: {yn_processor(nub.can_pin_messages)}"
        text += f"\nCan promote members to admins: {yn_processor(nub.can_promote_members)}"
    elif s == "member":
        text += f"\n\n*Member* of {title}"
    elif s == "restricted":
        text += f"\n\n*Restricted* in {title}"
        text += f"\n\nCan send messages: {yn_processor(nub.can_send_messages)}"
        if nub.can_send_messages:
            text += f"\nCan send media: {yn_processor(nub.can_send_media_messages)}"
            if nub.can_send_media_messages:
                text += f"\nCan send stickers and GIFs: {yn_processor(nub.can_send_other_messages)}"
                text += f"\nCan add web page previews: {yn_processor(nub.can_add_web_page_previews)}"
    elif s == "left":
        text += f"\n\n*Previously a member* of {title}"
    elif s == "kicked":
        text += f"\n\n*Banned* from {title}"
    msg.reply_markdown(text)


def get_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if rmsg:
        ff = rmsg.forward_from
        if ff:
            msg.reply_markdown(f"User id of original message's sender: `{ff.id}`")
        else:
            msg.reply_markdown(f"`{rmsg.from_user.id}`")
    else:
        user_id = msg.from_user.id
        if msg.chat_id > 0:
            msg.reply_markdown(f"`{user_id}`")
        else:
            msg.reply_markdown(f"Chat id: `{msg.chat_id}`\nYour user id: `{user_id}`")


def get_message_link(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        msg.reply_text("no u, reply to a message")
        return
    chat = msg.chat
    if chat.type == Chat.SUPERGROUP and chat.username:
        msg.reply_text(f"https://t.me/{chat.username}/{rmsg.id}", disable_web_page_preview=True)
    else:
        msg.reply_markdown(f"no u, can only use in public supergroup, but the message id is `{rmsg.id}`.")


def get_file_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        msg.reply_text("no u, reply to a message")
        return
    if rmsg.audio:
        gfi_response(msg, "audio", rmsg.audio.file_id)
    elif rmsg.photo:
        gfi_response(msg, "picture", rmsg.photo[-1].file_id)
    elif rmsg.sticker:
        gfi_response(msg, "sticker", rmsg.sticker.file_id)
    elif rmsg.video:
        gfi_response(msg, "video", rmsg.video.file_id)
    elif rmsg.voice:
        gfi_response(msg, "voice recording", rmsg.voice.file_id)
    elif rmsg.video_note:
        gfi_response(msg, "video", rmsg.video_note.file_id)
    elif rmsg.document:
        gfi_response(msg, "document", rmsg.document.file_id)
    else:
        msg.reply_text("no u, message has no media.")


def gfi_response(msg, file_type, file_id):
    msg.reply_markdown(f"File id of this {file_type}: `{file_id}`")


def ping(bot, update):
    update.message.reply_markdown("Ping your mother?!")


def pinned(bot, update):
    msg = update.message
    chat = msg.chat
    if chat.type != Chat.SUPERGROUP:
        msg.reply_text("no u, supergroups only")
        return
    chat.send_action("typing")
    chat_info = bot.get_chat(chat.id)
    pmsg = chat_info.pinned_message
    if not pmsg:
        msg.reply_text("no u, no pinned (can be wrong, especially if the pinned message is sent by bots, "
                       "unstable function)")
        return
    p_id = pmsg.message_id
    if not pmsg.from_user.is_bot or pmsg.from_user.id == bot.id:
        pmsg.reply_text("⬆️Pinned message⬆️")
    elif chat.username:
        link = f"https://t.me/{chat.username}/{p_id}"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Pinned message", url=link)]])
        msg.reply_text("⬇️Pinned message⬇️", reply_markup=reply_markup)
    else:
        msg.reply_text(f"no u, sender is bot and group is private, but the id of that message is `{p_id}`.")


def check_number_dude(msg, user, is_new=False):
    if user.last_name and len(user.first_name) == len(user.last_name) == 8:
        if user.first_name.isdigit() and user.last_name.isdigit():
            msg.reply_text("Number man, on9. Ban!!!")
            try:
                msg.chat.kick_member(user.id)
            except TelegramError:
                pass
            if not is_new:
                del_msg(msg)
            return True


def message_handler(bot, update):
    msg = update.message
    user = msg.from_user
    if msg.new_chat_members:
        for nub in msg.new_chat_members:
            if nub.id == bot.id:
                msg.reply_markdown(f"Use /help to see my functions. Contact {OWNER_MENTION} if you have questions, "
                                   "suggestions or found typos or errors.")
            elif nub.is_bot:
                msg.reply_text("Ooh, new bot!")
            else:
                check_number_dude(msg, nub, is_new=True)
    elif msg.left_chat_member:
        msg.reply_text("Bey.")
    elif check_number_dude(msg, msg.from_user):
        return
    elif msg.text:
        text = msg.text.lower()
        if user.id == OWNER_ID and text == "hello":
            msg.reply_text(f"Hi {OWNER_NAME}! Would you like JS with Spaghetti or Double Decker JS Hamburger for lunch?")
        elif user.id != OWNER_ID and msg.chat_id < 0 and OWNER_USERNAME.lower() in text:
            msg.reply_text("Tag your mother?!")
        elif user.id != OWNER_ID and [word for word in OWNER_NICKNAMES if word in text] and [word for word in INSULTS if word in text]:
            msg.reply_markdown("I got this error when I tried dividing your IQ by itself:\n"
                               "`Traceback (most recent call last):\n  File \"<input>\", line 777, in <module>\n"
                               "ZeroDivisionError: division by zero`")
        elif "ur mom gay" in text:
            msg.reply_text("no u")
        elif text == "no u":
            msg.reply_text("no no u")
        elif text == "no no u":
            msg.reply_text("no no no u")
        elif "no no no u" in text:
            msg.reply_sticker("CAADBAADSgIAAvkw6QXmVrbEBht6SAI")
        elif text == "js is very on9":
            msg.reply_text("Your IQ is 500!")
        elif text == f"trainer jono is rubbish":
            msg.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")
        elif "but can you do this" in text:
            msg.reply_sticker("CAADBAADbwIAAvkw6QUeD3c89PLAOAI")
        elif text == "goodest english":
            msg.reply_voice("AwADBQADJgAD8KLQVNdHdLAHdLMzAg")
        elif text == "my english is very good":
            msg.reply_voice("AwADBQADJwAD8KLQVFu-e5gh4i8RAg")
        elif "too good" in text or "very good" in text:
            msg.reply_voice("AwADBQADKAAD8KLQVHrlKTFsd-qGAg")


def owner_edit(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if msg.from_user.id != OWNER_ID:
        msg.reply_text("no u")
    elif not rmsg:
        msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != BOT_ID:
        msg.reply_text("no u, not my message")
    else:
        try:
            rmsg.edit_text(msg.split(maxsplit=1)[1])
        except TimedOut:
            pass
        except TelegramError as e:
            msg.reply_markdown(escape_markdown(str(e)))
        del_msg(msg)


def owner_delmsg(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if msg.from_user.id != OWNER_ID:
        msg.reply_text("no u")
    elif not rmsg:
        msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != BOT_ID:
        msg.reply_text("no u, not my message")
    else:
        del_msg(rmsg)
        del_msg(msg)


def feedback(bot, update):
    msg = update.message
    user = msg.from_user
    chat = msg.chat
    try:
        chat_link = f"https://t.me/{chat.username}" if chat.username and chat.id < 0 else None
        chat_name = f"[{chat.title}]({chat_link}) (chat id: `{chat.id}`)" if chat.id < 0 else "pm"
        fb = escape_markdown(msg.text.split(maxsplit=1)[1])
        fb = f"Feedback for {BOT_USERNAME} from {user.mention_markdown(user.full_name)} (user id: `{user.id}`) " \
             f"sent in {chat_name}:\n\n{fb}"
        if chat_link:
            message_link = f"{chat_link}/{msg.message_id}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Message", url=message_link)]])
            ADMIN_GROUP.send_message(fb, parse_mode=ParseMode.MARKDOWN,
                                     reply_markup=reply_markup, disable_web_page_preview=True)
        else:
            ADMIN_GROUP.send_message(fb, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
        msg.reply_text("Feedback sent successfully!")
    except IndexError:
        msg.reply_text("no u, put some constructive text behind it")


def error_handler(bot, update, error):
    try:
        if str(error) == "Timed out":
            return
        logger.warning(f'Update "{update}" caused error "{error}"')
        msg = update.message
        chat = msg.chat
        error = escape_markdown(str(error))
        forwarded = msg.forward(ADMIN_GROUP_ID)
        chat_link = f"https://t.me/{chat.username}" if chat.username and chat.id < 0 else None
        chat_name = f"[{chat.title}]({chat_link}) (chat id: `{chat.id}`)" if chat.id < 0 else "pm"
        text = f"Error occurred in {chat_name}:\n\n{error}"
        if chat_link:
            message_link = f"{chat_link}/{msg.message_id}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Message", url=message_link)]])
            forwarded.reply_markdown(text, reply_markup=reply_markup, disable_web_page_preview=True)
        else:
            forwarded.reply_markdown(text, disable_web_page_preview=True)
        forwarded.reply_markdown(f"Error: {error}, happened in {chat_name}", quote=True)
        msg.reply_text(f"This message caused an error: {error}\nThe message was forwarded to the creator and he will "
                       "try to fix it.")
    except TelegramError:
        pass


def main():
    debug = os.environ.get('DEBUG', "no")
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9js", tag9js))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("remove_keyboard2", remove_keyboard2))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("file_id", get_file_id))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("user_info", user_info))
    dp.add_handler(CommandHandler("pinned", pinned))
    dp.add_handler(CommandHandler("edit", owner_edit))
    dp.add_handler(CommandHandler("delmsg", owner_delmsg))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(CommandHandler("r", echo, allow_edited=True))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True, allow_edited=True))
    dp.add_handler(MessageHandler(Filters.chat(chat_id=-1001295361187), message_handler, edited_updates=True))
    dp.add_error_handler(error_handler)
    if debug != "yes":
        port = os.environ.get('PORT', 80)
        updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=BOT_TOKEN, clean=True)
        updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}")
    else:
        updater.start_polling(clean=True)
    updater.idle()


if __name__ == "__main__":
    main()
