from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import TelegramError, BadRequest, TimedOut
from telegram.utils.helpers import escape_markdown
from time import sleep
from re import match
import logging
import os


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "506548905:AAFCkZ5SI9INLEb0fwRHRlEji4Or6s8B9DQ"


def start(bot, update):
    msg = update.message
    if msg.chat_id > 0:
        msg.reply_text("Use /help to see my functions. Contact @Trainer_Jono if you have questions, suggestions or "
                       "found a typo or error, lol.")


def bot_help(bot, update):
    update.message.reply_markdown("[On9Bot功能](http://telegra.ph/On9Bot-Help-03-25) (尚未完成)\n"
                                  "[source code link placeholder]()\n"
                                  "¯\\\_(ツ)\_/¯")


@run_async
def tag9js(bot, update):
    msg = update.message
    chat = update.effective_chat
    if chat.id == -1001295361187:
        chat.send_action("typing")
        js_info = chat.get_member(190726372)
        if js_info.user.username:
            sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                                  reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]))
            sleep(15)
            msg.reply_text("Tag9js over, keyboard removed, message deleted.",
                           reply_markup=ReplyKeyboardRemove(), quote=False)
            try:
                sent.delete()
            except TelegramError:
                pass
        else:
            msg.reply_text("no u, JS removed his username.")
    elif chat.id < 0:
        msg.reply_text("no u")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Join HK Duker", url="https://t.me/hkduker")]])
        msg.reply_text("This command can only be used in HK Duker. You are welcome to join us and of course, try out "
                       "the command.", reply_markup=reply_markup)


can_use_tag9 = (463998526, 190726372, 106665913)
# respectively  Tr. Jono,  JS,        Jeffffffc
temp_can_use_tag9 = (534780193, 444970538)
# Re 2's accounts


@run_async
def tag9(bot, update, args):
    msg = update.message
    chat = msg.chat
    chat.send_action("typing")
    if not (msg.from_user.id in can_use_tag9 or msg.from_user.id in temp_can_use_tag9):
        msg.reply_text("no u")
    elif msg.chat_id > 0:
        msg.reply_text("no u")
    elif msg.reply_to_message:
        tag9_part2(msg, chat.get_member(msg.reply_to_message.from_user.id))
    elif not args:
        msg.reply_text("Please reply to an user's message or provide a valid user id as an argument.")
    else:
        try:
            tag9_part2(msg, chat.get_member(int(args[0])))
        except ValueError:
            msg.reply_text("no u, user ids only.")
        except BadRequest as e:
            msg.reply_text("no u")


@run_async
def tag9_part2(msg, u_info):
    if u_info.status in ("restricted", "left", "kicked"):
        msg.reply_text("no u, not in group or restricted")
    elif u_info.user.id in (463998526, 506548905):
        msg.reply_text("no u")
    elif u_info.user.is_bot:
        msg.reply_text("no u, dun tag other bots.")
    elif u_info.user.username is None:
        msg.reply_text("no u, no username.")
    else:
        sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                              reply_markup=ReplyKeyboardMarkup([[u_info.user.name]]))
        sleep(15)
        msg.reply_text("Tag9 over, keyboard removed, message deleted.", reply_markup=ReplyKeyboardRemove(), quote=False)
        try:
            sent.delete()
        except TelegramError:
            pass


def remove_keyboard(bot, update):
    msg = update.message
    if msg.chat_id < 0:
        msg.reply_text("Keyboard removed.", reply_markup=ReplyKeyboardRemove())
    else:
        msg.reply_text("no u")


def check_number_dude(bot, update, user):
    msg = update.message
    if match(r'\d\d\d\d\d\d\d\d', user.first_name) and match(r'\d\d\d\d\d\d\d\d', user.last_name):
        msg.reply_text("Number man, shit. BAN!!!!")
        try:
            msg.chat.kick_member(user.id)
        except TelegramError:
            pass
        try:
            msg.delete()
        except TelegramError:
            pass
        return True


markdown_error_text = """no u, markdown error: {}.
Parse mode = Markdown. Use a backslash (\"\\\") before a markdown character to escape it, like this:
\"\_\", \"\*\", \"\`" """


def echo(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    try:
        args = msg.text.split(" ", 1)[1]
        if msg.reply_to_message:
            try:
                rmsg.reply_markdown(args, disable_web_page_preview=True)
            except BadRequest as e:
                msg.reply_text(markdown_error_text.format(str(e)))
            else:
                try:
                    msg.delete()
                except TelegramError:
                    pass
        else:
            try:
                msg.reply_markdown(args, disable_web_page_preview=True, quote=False)
            except TelegramError as e:
                msg.reply_text(markdown_error_text.format(str(e)))
            else:
                try:
                    msg.delete()
                except TelegramError:
                    pass
    except IndexError:
        if rmsg:
            if rmsg.text:
                try:
                    msg.reply_text(rmsg.text, disable_web_page_preview=True,
                                   quote=False)
                except TelegramError as e:
                    msg.reply_text(markdown_error_text.format(str(e)))
                else:
                    try:
                        msg.delete()
                    except TelegramError:
                        pass
            else:
                msg.reply_text("no u, messages with text only.")
        else:
            msg.reply_markdown("no u, use `/echo [text]` or reply to a message.")


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
    if user.is_bot:
        text = "*Information of this bot*"
    else:
        text = "*Information of this user*"
    text += "\n\nUser id: `{}`\nName: {}".format(user.id, escape_markdown(user.full_name))
    if user.username:
        text += "\nUsername: @{}".format(escape_markdown(user.username))
    if user.language_code:
        text += "\nLanguage code: {}".format(user.language_code)
    try:
        nub = chat.get_member(user.id)
        status = nub.status
    except TelegramError:
        msg.reply_text(text)
        return
    if status == "creator":
        text += "\n\n*Creator* of {}".format(title)
    elif status == "administrator":
        text += "\n\n*Administrator* of {}".format(title)
        if nub.can_change_info:
            text += "\n\nCan change group info: Yes"
        else:
            text += "\n\nCan change group info: No"
        if nub.can_delete_messages:
            text += "\nCan delete messages: Yes"
        else:
            text += "\nCan delete messages: No"
        if nub.can_restrict_members:
            text += "\nCan restrict, ban and unban members: Yes"
        else:
            text += "\nCan restrict, ban and unban members: No"
        if nub.can_pin_messages:
            text += "\nCan pin messages: Yes"
        else:
            text += "\nCan pin messages: No"
        if nub.can_promote_members:
            text += "\nCan add new admins: Yes"
        else:
            text += "\nCan add new admins: No"
    elif status == "member":
        text += "\n\n*Member* of {}".format(title)
    elif status == "restricted":
        text += "\n\n*Restricted* in {}".format(title)
        if nub.can_send_messages:
            text += "\n\nCan send messages: Yes"
            if nub.can_send_media_messages:
                text += "\nCan send media: Yes"
                if nub.can_send_other_messages:
                    text += "\nCan send stickers and GIFs: Yes"
                else:
                    text += "\nCan send stickers and GIFs: No"
                if nub.can_add_web_page_previews:
                    text += "\nCan add web page previews: Yes"
                else:
                    text += "\nCan add web page previews: No"
            else:
                text += "\nCan send media: No"
        else:
            text += "\n\nCan send messages: No"
    elif status == "left":
        text += "\n\n*Previously a member* of {}".format(title)
    elif status == "kicked":
        text += "\n\n*Banned* from {}".format(title)
    msg.reply_markdown(text)


def get_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if rmsg:
        msg.reply_markdown("This user's id: `{}`".format(rmsg.from_user.id))
    else:
        msg.reply_markdown("This chat's id: `{}`\nYour id: `{}`".format(msg.chat_id, msg.from_user.id))


def get_message_link(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        msg.reply_text("no u")
        return
    chat = msg.chat
    if chat.type == "supergroup" and chat.username:
        msg.reply_text("https://telegram.dog/{}/{}".format(chat.username, rmsg.id), disable_web_page_preview=True)
    else:
        msg.reply_markdown("no u, can only use in public supergroup, but its message id is ```{}```.".format(rmsg.id))


def get_file_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        msg.reply_text("no u")
        return
    if rmsg.audio:
        get_file_id_response(msg, "audio", rmsg.audio.file_id)
    elif rmsg.photo:
        get_file_id_response(msg, "picture", rmsg.photo[-1].file_id)
    elif rmsg.sticker:
        get_file_id_response(msg, "sticker", rmsg.sticker.file_id)
    elif rmsg.video:
        get_file_id_response(msg, "video", rmsg.video.file_id)
    elif rmsg.voice:
        get_file_id_response(msg, "voice recording", rmsg.voice.file_id)
    elif rmsg.video_note:
        get_file_id_response(msg, "video", rmsg.video_note.file_id)
    elif rmsg.document:
        get_file_id_response(msg, "document", rmsg.document.file_id)
    else:
        msg.reply_text("no u, message has no media.")


def get_file_id_response(msg, file_type, file_id):
    msg.reply_markdown("File id of this {}: `{}`".format(file_type, file_id))


def ping(bot, update):
    update.message.reply_markdown("Ping your mother?!")


def pinned(bot, update):
    msg = update.message
    chat = msg.chat
    if chat.type != "supergroup":
        msg.reply_text("no u, supergroups only")
        return
    chat.send_action("typing")
    chat_info = bot.get_chat(chat.id)
    pmsg = chat_info.pinned_message
    if not pmsg:
        msg.reply_text("no u, no pinned (may be outdated)")
        return
    p_id = pmsg.message_id
    if not pmsg.from_user.is_bot or pmsg.from_user.id == 506548905:
        msg.reply_text("⬆️Pinned message⬆️", reply_to_message_id=p_id)
    elif chat.username:
        link = "https://telegram.dog/{}/{}".format(chat.username, p_id)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Pinned message", url=link)]])
        msg.reply_text("⬇️Pinned message⬇️", reply_markup=reply_markup)
    else:
        msg.reply_text("no u, sender is bot and group is private, but the id of that message is `{}`.".format(p_id))


def message_handler(bot, update):
    msg = update.message
    user = update.effective_user
    if msg.new_chat_members:
        for nub in msg.new_chat_members:
            if nub.id == 506548905:
                msg.reply_markdown("Use /help to see my functions. Contact @Trainer_Jono if you have questions, "
                                   "suggestions or found typos/errors, lol.")
            elif nub.is_bot:
                msg.reply_text("Ayy, new bot!")
            else:
                check_number_dude(bot, update, nub)
    elif msg.left_chat_member:
        msg.reply_text("Bey.")
    elif check_number_dude(bot, update, msg.from_user):
        return
    elif msg.text:
        text = msg.text.lower()
        if text == "hello" and user.id == 463998526:
            msg.reply_text("主人你好！")
        elif user.id != 463998526 and msg.chat_id < 0 and "@trainer_jono" in text:
            msg.reply_text("唔好tag我主人，乖。")
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
        chat_link = "telegram.dog/{}".format(chat.username) if chat.username and chat.id < 0 else None
        chat_name = "[{}]({}) (chat id: `{}`)".format(chat.title, chat_link, chat.id) if chat.id < 0 else "pm"
        fb = escape_markdown(msg.text.split(" ", 1)[1])
        fb = "\n\nFeedback for @On9Bot from {} (user id: `{}`) sent in {}:\n\n{}".format(
            user.mention_markdown(user.full_name), user.id, chat_name, fb)
        if chat_link:
            message_link = chat_link + "/" + str(msg.message_id)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Message", url=message_link)]])
            bot.send_message(-1001141544515, fb, parse_mode="Markdown",
                             reply_markup=reply_markup, disable_web_page_preview=True)
        else:
            bot.send_message(-1001141544515, fb, parse_mode="Markdown", disable_web_page_preview=True)
        msg.reply_text("Feedback sent successfully!")
    except IndexError:
        msg.reply_text("no u, put some constructive text behind it")


def error_handler(bot, update, error):
    if str(error) == "Timed out":
        return
    logger.warning('Update "%s" caused error "%s"', update, error)
    msg = update.message
    error = escape_markdown(str(error))
    forwarded = msg.forward(-1001141544515)
    forwarded.reply_text("Error: {}".format(error), quote=True)
    msg.reply_text("This message caused an error: {}\nThe message was forwarded to the creator and he will try to "
                   "fix it.".format(error))


def main():
    name = "on9bot"
    port = os.environ.get("PORT")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9js", tag9js))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("file_id", get_file_id))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("r", echo))
    dp.add_handler(CommandHandler("user_info", user_info))
    dp.add_handler(CommandHandler("pinned", pinned))
    dp.add_handler(CommandHandler("feedback", feedback))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, message_handler))
    dp.add_error_handler(error_handler)
    updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=TOKEN, clean=True)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(name, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
