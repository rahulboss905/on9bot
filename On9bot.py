from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest, TimedOut
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
# temp_can_use_tag9 = (487754154, 426072433, 49202743, 442517724)
# respectively       Cat,       Giselle,   Siu Kei,  Chestnut,


@run_async
def tag9(bot, update, args):
    msg = update.message
    chat = msg.chat
    chat.send_action("typing")
    if msg.from_user.id not in can_use_tag9:  # and msg.from_user.id not in can_use_tag9:
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
            msg.reply_text("no u, numbers only")
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
        msg.reply_text("no u, no username.")
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
            msg.chat.kick_member(user.id)
        except Exception:
            pass
        try:
            msg.delete()
        except Exception:
            pass
        return True


markdown_error_text = """Markdown error: {}
Parse mode is Markdown. Use a backslash (\"\\\") before a markdown character (\"_\", \"*\", \"`") to escape it."""


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
                except Exception:
                    pass
        else:
            try:
                msg.reply_markdown(args, disable_web_page_preview=True, quote=False)
            except Exception as e:
                msg.reply_text(markdown_error_text.format(str(e)))
            else:
                try:
                    msg.delete()
                except Exception:
                    pass
    except IndexError:
        if rmsg:
            if rmsg.text:
                try:
                    msg.reply_text(rmsg.text, disable_web_page_preview=True,
                                   quote=False)
                except Exception as e:
                    msg.reply_text(markdown_error_text.format(str(e)))
                else:
                    try:
                        msg.delete()
                    except Exception:
                        pass
            else:
                msg.reply_text("no u")
        else:
            msg.reply_text("no u")


def user_info(bot, update):
    msg = update.message
    if not msg.reply_to_message:
        msg.reply_text("no u, reply to a message")
        return
    if msg.chat_id > 0:
        msg.reply_text("暫時群組入，面先用到呢個指令，pm就收皮先。")
        return
    chat = msg.chat
    chat.send_action("typing")
    user = msg.reply_to_message.from_user
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
        nub = chat.get_member(user.id)
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
        text += "\n\n*Previously a member of {}".format(title)
    elif status == "kicked":
        text += "\n\n*Banned* from {}".format(title)
    msg.reply_markdown(text)


def get_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if rmsg:
        msg.reply_markdown("佢嘅user id: ```{}```".format(rmsg.from_user.id))
    else:
        msg.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```".format(msg.chat_id, msg.from_user.id))


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
        msg.reply_markdown("no u, can only use in public supergroup, but message id is ```{}```.".format(rmsg.id))


def get_file_id(bot, update):
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        msg.reply_text("no u")
        return
    if rmsg.audio:
        get_file_id_response(msg, "段音頻", rmsg.audio.file_id)
    elif rmsg.photo:
        get_file_id_response(msg, "張相", rmsg.photo[-1].file_id)
    elif rmsg.sticker:
        get_file_id_response(msg, "張貼紙", rmsg.sticker.file_id)
    elif rmsg.video:
        get_file_id_response(msg, "段影片", rmsg.video.file_id)
    elif rmsg.voice:
        get_file_id_response(msg, "段錄音", rmsg.voice.file_id)
    elif rmsg.video_note:
        get_file_id_response(msg, "段影片", rmsg.video_note.file_id)
    elif rmsg.document:
        get_file_id_response(msg, "份文件", rmsg.document.file_id)
    else:
        msg.reply_text("no u")


def get_file_id_response(msg, file_type, file_id):
    msg.reply_markdown("呢{}嘅file id: ```{}```".format(file_type, file_id))


def ping(bot, update):
    update.message.reply_markdown("Ping你老母？！")


def pinned(bot, update):
    msg = update.message
    chat = msg.chat
    if chat.type != "supergroup":
        msg.reply_text("no u, supergoups only")
        return
    chat_info = bot.get_chat(chat.id)
    if not chat_info.pinned_message:
        msg.reply_text("no u, no pinned (may be outdated)")
        return
    pmsg = chat_info.pinned_message
    p_id = pmsg.message_id
    if not pmsg.from_user.is_bot or pmsg.from_user.id == 506548905:
        msg.reply_text("⬆️Pinned message⬆️)", reply_to_message_id=p_id)
        return
    if chat.username:
        link = "https://telegram.dog/{}/{}".format(chat.username, p_id)
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Pinned message", url=link)]])
        msg.reply_text("⬇️Pinned message⬇️)", reply_markup=reply_markup)
        return
    msg.reply_text("no u, sender is bot and supergroup is private, cannot help")


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
    elif msg.left_chat_member:
        msg.reply_text("Bey")
    elif check_number_dude(bot, update, msg.from_user):
        return
    # if msg.pinned_message:
    #     if user.id != 463998526:
    #         msg.reply_markdown(user.mention_markdown(user.full_name) + "又pin嘢...🙃", quote=False)
    # elif msg.sticker:
    #     if msg.sticker.set_name in ("payize2", "FPbabydukeredition"):
    #         msg.reply_text("嘩屌又係bb，見到都反胃。")
    elif msg.text:
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
    chat = msg.chat
    try:
        chat_link = "telegram.dog/{}".format(chat.username) if chat.username and chat.id < 0 else None
        chat_name = "[{}]({}) (chat id: `{}`)".format(chat.title, chat_link, chat.id) if chat.id < 0 else "pm"
        fb = helpers.escape_markdown(msg.text.split(" ", 1)[1])
        fb = "\n\nFeedback from {} (user id: `{}`) sent in {} ({}).\n\n{}".format(user.mention_markdown(user.full_name),
                                                                                  user.id, chat_name, chat.type, fb)
        if chat_link:
            message_link = chat_link + "/" + str(msg.message_id)
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Feedback", url=message_link)]])
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
    forwarded = bot.forward_message(-1001141544515, update.effective_chat.id, update.message.message_id)
    bot.send_message(-1001141544515, str(error), reply_to_message_id=forwarded.message_id)


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
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(name, TOKEN))
    updater.idle()


if __name__ == "__main__":
    main()
