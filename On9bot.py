from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest
from telegram.utils import helpers
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
        msg.reply_text("吓。求其揾個command用下，撳 /help 睇點用。有咩事揾 @Trainer_Jono 。")


def bot_help(bot, update):
    update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25) (尚未完成)\n"
                                  "[Source code](https://www.codepile.net/pile/3aD3DPkD) (尚未更新)\n"
                                  "¯\\\_(ツ)\_/¯")


@run_async
def tag9js(bot, update):
    msg = update.message
    chat = update.effective_chat
    if chat.id == -1001295361187:
        chat.send_action(ChatAction.TYPING)
        js_info = chat.get_member(190726372)
        if js_info.user.username:
            sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                                  reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]))
            sleep(15)
            msg.reply_text("Tag9js is over, keyboard removed, message deleted.", reply_markup=ReplyKeyboardRemove(), quote=False)
            try:
                sent.delete()
            except Exception:
                pass
        else:
            msg.reply_text("no u, JS removed his username.")
    elif chat.id < 0:
        msg.reply_text("no u")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
        msg.reply_text("呢個指令只可以喺HK Duker用，歡迎撳下面個掣入嚟HK Duker一齊 /tag9js 。", reply_markup=reply_markup)


can_use_tag9 = (463998526, 190726372, 106665913)
# respectively  Tr. Jono,  JS,        Jeffffffc
temp_can_use_tag9 = (487754154, 426072433, 49202743, 442517724)
# respectively       Cat,       Giselle,   Siu Kei,  Chestnut,


@run_async
def tag9(bot, update, args):
    msg = update.message
    update.effective_chat.send_action(ChatAction.TYPING)
    if msg.from_user.id not in can_use_tag9 and msg.from_user.id not in can_use_tag9:
        msg.reply_text("no u")
    elif msg.chat_id > 0:
        msg.reply_text("no u")
    elif msg.reply_to_message:
        tag9_part2(msg, bot.get_chat_member(msg.chat_id, msg.reply_to_message.from_user.id))
    elif not args:
        msg.reply_text("Please reply to an user's message or provide a valid user id as an argument.")
    else:
        try:
            tag9_part2(msg, bot.get_chat_member(msg.chat_id, int(args[0])))
        except ValueError:
            msg.reply_text("no u")
        except BadRequest as e:
            msg.reply_text("Bad request: " + str(e))


@run_async
def tag9_part2(msg, u_info):
    if u_info.status in ("restricted", "left", "kicked"):
        msg.reply_text("no u, not in group or restricted")
    elif u_info.user.id in (463998526, 506548905):
        msg.reply_text("no u")
    elif u_info.user.is_bot:
        msg.reply_text("no u, dun tag other bots")
    elif u_info.user.username is None:
        msg.reply_markdown("no u, no username.")
    else:
        sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                              reply_markup=ReplyKeyboardMarkup([[u_info.user.name]]))
        sleep(15)
        msg.reply_text("Tag9 over, keyboard removed, message deleted.", reply_markup=ReplyKeyboardRemove(), quote=False)
        try:
            sent.delete()
        except Exception:
            pass


def remove_keyboard(bot, update):
    msg = update.message
    if msg.chat_id < 0:
        msg.reply_text("Keyboard removed.", reply_markup=ReplyKeyboardRemove())
    else:
        msg.reply_text("no u")


cn_swear_words = ("屌", "閪", "柒", "撚", "鳩", "𨳒", "屄", "𨶙", "𨳊", "㞗", "𨳍", "杘")
cn_swear_words_in_eng = ("diu", "dllm", "dnlm")
eng_swear_words = ("anus", "arse", "ass", "axwound", "bampot", "bastard", "beaner", "bitch", "blowjob", "bollocks",
                   "bollox", "boner", "butt", "camaltoe", "carpetmuncher", "chesticle", "chinc", "chink", "choad",
                   "chode", "clit", "cock", "coochie", "choochy", "coon", "cooter", "cracker", "cum", "cunnie",
                   "cunnilingus", "cunt", "dago", "damn", "deggo", "dick", "dike", "dildo", "doochbag", "dookie",
                   "douche", "dumb", "dyke", "fag", "fellatio", "feltch", "flamer", "fuck", "fidgepacker",
                   "goddamn", "goddamnit", "gooch", "gook", "gringo", "guido", "handjob", "hardon", "heeb", "hell",
                   "hoe", "homo", "honkey", "humping", "jagoff", "jap", "jerk", "jigaboo", "jizz", "junglebunny",
                   "kike", "kooch", "kootch", "kraut", "kunt", "kyke", "lesbian", "lesbo", "lezzie", "mick", "minge",
                   "muff", "munging", "negro", "nigaboo", "nigga", "nigger", "niglet", "nutsack", "paki", "panooch",
                   "pecker", "penis", "piss", "polesmoker", "pollock", "poon", "porchmonkey", "prick", "punanny",
                   "punta", "pussy", "pussies", "puto", "queef", "queer", "renob", "rimjob", "ruski", "schlong",
                   "scrote", "shit", "shiz", "skank", "skeet", "slut", "smeg", "snatch", "spic", "splooge", "spook",
                   "tard", "thot", "testicle", "tit", "twat", "vajj", "vag", "vajayjay", "vjayjay", "wank", "wetback",
                   "whore", "wop", "wtf", "fk", "asshole", "bullshit", "shitty", "asshole")


def swear_word_detector(bot, update):
    msg = update.message
    text = msg.text
    if any(word in text for word in cn_swear_words):
        msg.reply_text("講粗口？！記你一次大過！") if msg.chat_id < 0 else msg.reply_text("PM講粗口姐，我先懶得理你。Zzz...")
    else:
        text = text.lower().split(" ")
        if any(word in text for word in cn_swear_words_in_eng) or any(word in text for word in eng_swear_words):
            msg.reply_text("講粗口？！記你一次大過！") if msg.chat_id < 0 else msg.reply_text("PM講粗口姐，我先懶得理你。Zzz...")


def check_number_dude(bot, update, user):
    msg = update.message
    if match(r'\d\d\d\d\d\d\d\d', user.first_name) and match(r'\d\d\d\d\d\d\d\d', user.last_name):
        msg.reply_text("又係數字人？我屌！")
        try:
            update.effective_chat.kick_member(user.id)
        except Exception:
            pass
        try:
            msg.delete()
        except Exception:
            pass


def markdown_error_response(error):
    text = """Markdown error: {}
Parse mode is Markdown. Use a backslash (\"\\\") before a markdown character (\"_\", \"*\", \"`") to escape it.""".format(str(error))
    return text


def echo(bot, update):
    msg = update.message
    try:
        args = msg.text.split(" ", 1)[1]
        if msg.reply_to_message:
            try:
                msg.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
            except Exception as e:
                msg.reply_text(markdown_error_response(e))
            else:
                try:
                    msg.delete()
                except Exception:
                    pass
        else:
            try:
                msg.reply_markdown(args, disable_web_page_preview=True, quote=False)
            except Exception as e:
                msg.reply_text(markdown_error_response(e))
            else:
                try:
                    msg.delete()
                except Exception:
                    pass
    except IndexError:
        if update.message.reply_to_message:
            if msg.reply_to_message.text:
                try:
                    msg.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                   quote=False)
                except Exception as e:
                    msg.reply_text(markdown_error_response(e))
                else:
                    try:
                        msg.delete()
                    except Exception:
                        pass
            else:
                msg.reply_to_message.reply_text("no u")
        else:
            msg.reply_text("""Deez r da waes:
/r <text>
/r [reply to a text message (files with captions don't count) not sent by other bots]
/r <text> [reply to a message not sent by other bots]
More info in /help.""")


def user_info(bot, update):
    msg = update.message
    if not msg.reply_to_message:
        msg.reply_text("Dis is da wae: /user_info [reply to a message]")
        return
    if msg.chat_id > 0:
        msg.reply_text("暫時群組入，面先用到呢個指令，pm就收皮先。")
        return
    user = msg.reply_to_message.from_user
    chat = update.effective_chat
    title = chat.title
    if user.is_bot:
        text = "*Information of this bot*"
    else:
        text = "*Information of this user*"
    text += "\n\nUser id: `{}`\nName: {}".format(user.id, helpers.escape_markdown(user.full_name))
    if user.username:
        text += "\nUsername: @{}".format(helpers.escape_markdown(user.username))
    if user.language_code:
        text += "\nLanguage code: {}".format(user.language_code)
    try:
        nub = bot.get_chat_member(msg.chat_id, user.id)
        status = nub.status
    except Exception:
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
        text += "\n\n*Restricted* in {}*".format(title)
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
        text += "\n\n*Was a member of {}".format(title)
    elif status == "kicked":
        text += "\n\n*Banned* from {}".format(title)
    msg.reply_markdown(text)


def get_id(bot, update):
    msg = update.message
    if msg.reply_to_message:
        msg.reply_markdown("佢嘅user id: ```{}```".format(msg.reply_to_message.from_user.id))
    else:
        msg.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```".format(msg.chat_id, msg.from_user.id))


def get_message_link(bot, update):
    msg = update.message
    if not msg.reply_to_message:
        msg.reply_text("Reply to a message.")
        return
    chat = update.effective_chat
    rmsg_id = msg.reply_to_message.message_id
    if chat.type == "supergroup" and chat.username:
        msg.reply_text("t.me/{}/{}".format(chat.username, rmsg_id), disable_web_page_preview=True)
    else:
        msg.reply_markdown("公開嘅超級群組嘅訊息先有link㗎。不過我可以話你知，嗰條訊息嘅message id係```{}```。".format(rmsg_id))


def get_file_id(bot, update):
    msg = update.message
    if not msg.reply_to_message:
        msg.reply_text(get_file_id_error)
        return
    rmsg = msg.reply_to_message
    if rmsg.audio:
        get_file_id_response(bot, update, "段音頻", rmsg.audio.file_id)
    elif rmsg.photo:
        get_file_id_response(bot, update, "張相", rmsg.photo[-1].file_id)
    elif rmsg.sticker:
        get_file_id_response(bot, update, "張貼紙", rmsg.sticker.file_id)
    elif rmsg.video:
        get_file_id_response(bot, update, "段影片", rmsg.video.file_id)
    elif rmsg.voice:
        get_file_id_response(bot, update, "段錄音", rmsg.voice.file_id)
    elif rmsg.video_note:
        get_file_id_response(bot, update, "段影片", rmsg.video_note.file_id)
    elif rmsg.document:
        get_file_id_response(bot, update, "份文件", rmsg.document.file_id)
    else:
        msg.reply_text(get_file_id_error)


def get_file_id_response(bot, update, file_type, file_id):
    update.message.reply_markdown("呢{}嘅file id: ```{}```".format(file_type, file_id))


get_file_id_error = """Dis is da wae: /file_id [reply to message containing media or general files]
Supported file types include:
Audios (.mp3)
Documents (general files)
Photos (most image formats are supported)
Stickers (.webp)
Videos (.mp4)
Voice recordings (.ogg)
Video messages"""


def ping(bot, update):
    update.message.reply_markdown("Ping你老母？！")


def pinned(bot, update):
    msg = update.message
    chat = update.effective_chat
    if chat.type != "supergroup":
        msg.reply_text("This command can only be used in supergroups!")
        return
    chat_info = bot.get_chat(chat.id)
    if not chat_info.pinned_message:
        msg.reply_text("No message is pinned in this supergroup currently (might be a few minutes out-of-date.")
        return
    pmsg_id = chat_info.pinned_message.message_id
    if not chat_info.pinned_message.from_user.is_bot or chat_info.pinned_message.from_user.id == 506548905:
        msg.reply_text("⬆️Pinned message (might be a few minutes out-of-date)⬆️", reply_to_message_id=pmsg_id)
        return
    if chat.username:
        link = "https://t.me/{}/{}".format(chat.username, pmsg_id)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Pinned message", url=link)]])
        msg.reply_text("The message is sent by another bot, so I can only provide you an url button to the message.\n\n"
                       "⬇️Pinned message (might be a few minutes out-of-date)⬇️", reply_markup=reply_markup)
        return
    msg.reply_text("The pinned message was sent by another bot and this supergroup is not public, so I cannot help you.")


def message_handler(bot, update):
    msg = update.message
    user = update.effective_user
    if msg.new_chat_members:
        for nub in msg.new_chat_members:
            if nub.id == 506548905:
                msg.reply_markdown("Hi，我係On9 Bot。撳 /help 睇點用。")
            elif nub.is_bot:
                msg.reply_text("哦？新bot喎，乜水？")
            else:
                check_number_dude(bot, update, nub)
        return
    elif msg.left_chat_member:
        msg.reply_text("Bey")
        return
    check_number_dude(bot, update, msg.from_user)
    # if msg.pinned_message:
    #     if user.id != 463998526:
    #         msg.reply_markdown(user.mention_markdown(user.full_name) + "又pin嘢...🙃", quote=False)
    # elif msg.sticker:
    #     if msg.sticker.set_name in ("payize2", "FPbabydukeredition"):
    #         msg.reply_text("嘩屌又係bb，見到都反胃。")
    if msg.text:  # change to elif when uncommenting the above code
        swear_word_detector(bot, update)
        text = msg.text.lower()
        if text == "hello" and user.id == 463998526:
            msg.reply_text("主人你好！")
        elif update.effective_user.id != 463998526 and msg.chat_id < 0 and "@trainer_jono" in text:
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
        elif "trainer jono is rubbish" in text:
            msg.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")


def feedback(bot, update):
    msg = update.message
    user = msg.from_user
    chat = update.effective_chat
    try:
        link = "telegram.dog/{}".format(chat.username) if chat.username else None
        chat_type = "[{}]({}) (chat id: `{}`)".format(chat.title, link, chat.id) if chat.id < 0 else "pm"
        fb = helpers.escape_markdown(msg.text.split(" ", 1)[1])
        fb += "\n\nFeedback from {} (user id: `{}`) sent in {}.".format(user.mention_markdown(user.full_name),
                                                                        user.id, chat_type)
        bot.send_message(-1001141544515, fb, parse_mode="Markdown", disable_web_page_preview=True)
        msg.reply_text("Feedback sent successfully!")
    except IndexError:
        update.message.reply_text("Please provide an argument. For example: /feedback 我覺得你可以加呢個功能...")


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
    bot.send_message(-1001141544515, str(error))


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
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=TOKEN, clean=True)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(name, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
