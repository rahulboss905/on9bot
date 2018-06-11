import os
import logging
import datetime
from time import sleep

import psycopg2
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, Chat
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, CallbackQueryHandler, Filters, run_async
from telegram.ext.filters import MergedFilter
from telegram.error import TelegramError, TimedOut
from telegram.utils.helpers import escape_markdown
from telegram.parsemode import ParseMode

from config import *
from utils import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

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
    msg = update.message
    if msg.chat_id > 0:
        msg.reply_markdown(f"Use /help to see my functions. Contact {OWNER_MENTION} if you have questions, "
                           "suggestions or found a typo or error.")


def bot_help(bot, update):
    update.message.reply_markdown(f"Look at the code [here]({GITHUB_SOURCE_CODE_LINK}) to learn how I work, lol")


@run_async
def tag9js(bot, update):
    msg = update.message
    chat = msg.chat
    if chat.id == -1001295361187 or msg.from_user.id == OWNER.id:
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
            sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                                  reply_markup=ReplyKeyboardMarkup([[text]]), quote=True)
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
        msg.reply_text("This command can only be used in HK Duker.", reply_markup=reply_markup)


def tag9(bot, update, args):
    msg = update.effective_message
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
            nub_id = int(args[0])
            assert nub_id > 0
            tag9_part2(msg, chat.get_member(nub_id))
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
    elif u_info.user.id in (OWNER.id, BOT.id):
        msg.reply_text("no u")
    elif u_info.user.is_bot:
        msg.reply_text("no u, don't tag other bots.")
    elif u_info.user.username is None:
        msg.reply_text("no u, user has no username.")
    else:
        sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                              reply_markup=ReplyKeyboardMarkup([[u_info.user.name]]))
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
    msg = update.effective_message
    rmsg = msg.reply_to_message
    try:
        text = msg.text.split(maxsplit=1)[1]
        try:
            if msg.from_user.id != OWNER.id:
                echo_owner_check(text)
            if rmsg:  # if message has args and replies to another message
                rmsg.reply_markdown(text, disable_web_page_preview=True)
            else:  # if message has args and does not reply to another message
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
            text = rmsg.text
            try:
                if msg.from_user.id != OWNER.id:
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
    chat = msg.chat
    chat.send_action("typing")
    user = msg.reply_to_message.from_user if msg.reply_to_message else msg.from_user
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
    msg = update.effective_message
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


def owner_edit(bot, update):
    msg = update.effective_message
    rmsg = msg.reply_to_message
    if msg.from_user.id != OWNER.id:
        msg.reply_text("no u")
    elif not rmsg:
        msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != BOT_ID:
        msg.reply_text("no u, not my message")
    else:
        try:
            rmsg.edit_text(msg.text.split(maxsplit=1)[1])
            del_msg(msg)
        except IndexError:
            msg.reply_text("no u, tell me what to edit")
        except TimedOut:
            pass
        except TelegramError as e:
            msg.reply_markdown(escape_markdown(str(e)))


def owner_delmsg(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if msg.from_user.id != OWNER.id:
        msg.reply_text("no u")
    elif not rmsg:
        msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != BOT_ID:
        msg.reply_text("no u, not my message")
    else:
        del_msg(rmsg)
        del_msg(msg)


def owner_exec(bot, update):
    msg = update.message
    try:
        assert msg.from_user.id == OWNER.id
        code = msg.text.split(maxsplit=1)[1]
        exec(code)
    except (AssertionError, IndexError):
        msg.reply_text("no u")
    except TimedOut:
        pass
    except Exception as e:
        msg.reply_markdown(f"An error ocurred: ```{str(e)}```")


def service_msg_handler(bot, update):
    msg = update.message
    if msg.new_chat_members:
        for nub in msg.new_chat_members:
            if nub.id == bot.id:
                msg.reply_markdown(f"Use /help to see my functions. Contact {OWNER_MENTION} if you have questions, "
                                   "suggestions or found typos or errors.", quote=False)
            elif nub.is_bot:
                msg.reply_text("Ooh, new bot!")
            elif check_number_man(nub):
                kick_member(msg.chat, nub.id)
    elif msg.left_chat_member:
        msg.reply_text("Bey.")


def number_man_handler(bot, update):
    msg = update.effective_message
    kick_member(msg.chat, msg.from_user)


def owner_msg_handler(bot, update):
    update.effective_message.reply_text(f"Hi {OWNER.full_name}! "
                                        "Would you like JS with Spaghetti or Double Decker JS Hamburger for lunch?")


def no_u_handler(bot, update):
    msg = update.effective_message
    text = msg.text.lower()
    no_count = len([word for word in text.split() if word == 'no'])
    if 100 > no_count > 0:
        msg.reply_text(f"{'no '*(no_count + 1)}u")
    else:
        msg.reply_sticker("CAADBAADSgIAAvkw6QXmVrbEBht6SAI")


def other_msg_handler(bot, update):
    msg = update.effective_message
    user = msg.from_user
    text = msg.text.lower()
    if user.id != OWNER.id and msg.chat_id < 0 and OWNER_USERNAME.lower() in text:
        msg.reply_text("Tag your mother?!")
    elif (user.id != OWNER_ID and [word for word in OWNER_NICKNAMES if word in text] and
          [word for word in INSULTS if word in text] or "ur mom gay" in text):
        msg.reply_text("no u")
    elif text == "js is very on9":
        msg.reply_text("Your IQ is 500!")
    elif text == "trainer jono is rubbish":
        msg.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")
    elif "but can you do this" in text:
        msg.reply_sticker("CAADBAADbwIAAvkw6QUeD3c89PLAOAI")
    elif text == "goodest english":
        msg.reply_voice("AwADBQADJgAD8KLQVNdHdLAHdLMzAg")
    elif text == "my english is very good":
        msg.reply_voice("AwADBQADJwAD8KLQVFu-e5gh4i8RAg")
    elif "too good" in text or "very good" in text:
        msg.reply_voice("AwADBQADKAAD8KLQVHrlKTFsd-qGAg")


def feedback(bot, update):
    msg = update.message
    user = msg.from_user
    chat = msg.chat
    try:
        chat_link = f"https://t.me/{chat.username}" if chat.username and chat.id < 0 else None
        chat_name = f"[{chat.title}]({chat_link}) (chat id: `{chat.id}`)" if chat.id < 0 else "pm"
        fb = escape_markdown(msg.text.split(maxsplit=1)[1])
        fb = (f"Feedback for {BOT_USERNAME} from {user.mention_markdown(user.full_name)} (user id: `{user.id}`) "
              f"sent in {chat_name}:\n\n{fb}")
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


jeff_bday_text = "".join("""為咗慶祝Jeff生日，JS將會捐錢比 @werewolfbot 同 @Mud9bot。你亦可以支持兩個bot嘅發展，只要撳
下面個掣就可以提高JS捐額HK$1(係咪好多呢)。全部人同我撳撳撳撳撳...\n\n捐額暫時為HK${}""".split("\n", 1))

HK_DUKER_ID = -1001295361187


# def jeff_bday_start():
#     reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Add HK$1", callback_data="jeff_bday_donate")]])
#     msg = bot.send_message(HK_DUKER_ID, jeff_bday_text.format(0), reply_markup=reply_markup)
#     try:
#         bot.pin_chat_message(HK_DUKER_ID, msg.message_id, disable_notification=True)
#     except TelegramError:
#         pass
#     cur = conn.cursor()
#     try:
#         cur.execute("INSERT INTO jeff_bday_temp VALUES (%s)", (msg.message_id,))
#         conn.commit()
#     finally:
#         cur.close()


def jeff_bday_donate(bot, update):
    query = update.callback_query
    query.answer()
    nub_id = query.from_user.id
    cur = conn.cursor()
    try:
        cur.execute("SELECT amount FROM jeff_bday_donate WHERE user_id = %s", (nub_id,))
        nub = cur.fetchone()
        if not nub:
            cur.execute("INSERT INTO jeff_bday_donate VALUES (%s, 1)", (nub_id,))
        else:
            cur.execute("UPDATE jeff_bday_donate SET amount = %s WHERE user_id = %s", (nub[0] + 1, nub_id))
        conn.commit()
    finally:
        cur.close()


@run_async
def jeff_bday_edit_msg_wait(bot, job):
    cur = conn.cursor()
    try:
        cur.execute("SELECT amount FROM jeff_bday_donate")
        amounts = cur.fetchall()
        cur.execute("SELECT msg_id FROM jeff_bday_temp")
        msg_id = cur.fetchone()[0]
    finally:
        cur.close()
    total = sum([a[0] for a in amounts])
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Add HK$1", callback_data="donate")]])
    try:
        bot.edit_message_text(jeff_bday_text.format(total), HK_DUKER_ID, msg_id, reply_markup=reply_markup)
    except TelegramError as e:
        pass


def jeff_bday_end(bot, job):
    cur = conn.cursor()
    try:
        cur.execute("SELECT amount FROM jeff_bday_donate")
        amounts = cur.fetchall()
        cur.execute("SELECT msg_id FROM jeff_bday_temp")
        msg_id = cur.fetchone()[0]
    finally:
        cur.close()
    bot.edit_reply_markup(chat_id=HK_DUKER_ID, message_id=msg_id)
    total = sum([a[0] for a in amounts])
    bot.send_message(-1001295361187, "活動完結！Jeff會收到JS HK${}嘅捐款。".format(total))
    job.job_queue.stop()


def sql(bot, update):
    msg = update.message
    if msg.from_user.id != 463998526:
        msg.reply_text("no u")
        return
    else:
        cur = conn.cursor()
        try:
            query = msg.text.split(" ", 1)[1]
        except IndexError:
            msg.reply_text("no u")
            return
        try:
            cur.execute(query)
            output = cur.fetchall()
            conn.commit()
            if output:
                msg.reply_markdown(escape_markdown(str(output)))
            else:
                msg.reply_markdown("No output was returned.")
        finally:
            cur.close()


INIT_DB_SQL = """CREATE TABLE IF NOT EXISTS jeff_bday_donate (user_id BIGINT UNIQUE NOT NULL, amount BIGINT NOT NULL);
CREATE TABLE IF NOT EXISTS jeff_bday_temp (msg_id BIGINT NOT NULL);"""


def main():
    cur = conn.cursor()
    try:
        cur.execute(INIT_DB_SQL)
        conn.commit()
    finally:
        cur.close()
    debug = os.environ.get('DEBUG', "no")
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(jeff_bday_donate))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True, allow_edited=True))
    dp.add_handler(CommandHandler("tag9js", tag9js, allow_edited=True))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("remove_keyboard2", remove_keyboard2))
    dp.add_handler(CommandHandler("r", echo, allow_edited=True))
    dp.add_handler(CommandHandler("id", get_id, allow_edited=True))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("pinned", pinned))
    dp.add_handler(CommandHandler("file_id", get_file_id))
    dp.add_handler(CommandHandler("user_info", user_info))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(CommandHandler("sql", sql, allow_edited=True))
    dp.add_handler(CommandHandler("exec", owner_exec, allow_edited=True))
    dp.add_handler(CommandHandler("edit", owner_edit, allow_edited=True))
    dp.add_handler(CommandHandler("delmsg", owner_delmsg))
    dp.add_handler(MessageHandler(Filters.status_update, service_msg_handler))
    dp.add_handler(MessageHandler(MergedFilter(Filters.chat(-1001295361187), MergedFilter(
        check_number_man_filter, bot_is_admin_filter)), number_man_handler, edited_updates=True))
    dp.add_handler(MessageHandler(MergedFilter(Filters.user(OWNER_ID), Filters.regex(r"^[Hh][Ee][Ll][Ll][Oo]$")),
                                  owner_msg_handler, edited_updates=True))
    dp.add_handler(RegexHandler(r".*([Nn][Oo])+ [Uu].*", no_u_handler, edited_updates=True))
    dp.add_handler(MessageHandler(Filters.text, other_msg_handler, edited_updates=True))
    dp.add_error_handler(error_handler)
    job_queue = updater.job_queue
    job_queue.run_repeating(jeff_bday_edit_msg_wait, 4)
    job_queue.run_once(jeff_bday_end, datetime.datetime(2018, 6, 12, 0, 0, 0))
    if debug != "yes":
        port = os.environ.get('PORT', 80)
        updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=BOT_TOKEN, clean=True)
        updater.bot.set_webhook(f"https://{HEROKU_APP_NAME}.herokuapp.com/{BOT_TOKEN}")
    else:
        updater.start_polling(clean=True)
    updater.idle()


if __name__ == "__main__":
    main()
