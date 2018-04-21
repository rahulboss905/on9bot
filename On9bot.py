# On9Bot (an annoying Cantonese Telegram bot) source code
# Uses Python 3 and the python-telegram-bot library, hosted on Heroku

from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest
from telegram.utils import helpers
from time import sleep
from re import match
import logging
import os

# import psycopg2

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# conn = psycopg2.connect(host="ec2-23-21-121-220.compute-1.amazonaws.com",
#                         database="ddqe8lueaue1pl", user="fttveeezgekmvf",
#                         password="948fc928d48ed553c738617c8a906b5efc5b86e97ceb42cbbc55839a92057889")
# cur = conn.cursor()


def start(bot, update):  # add args back later when commenting ww parts
    if update.message.chat_id > 0:
        # try:
        #     if args:
        #         if args.startswith("joinww_"):
        #             chat_id = int(args[0].split("_", 1)[1])
        #             try:
        #                 user = bot.get_chat_member(chat_id, update.effective_user.id)
        #                 if user.status in ("restricted", "kicked", "left"):
        #                     raise Exception
        #             except:
        #                 update.message.reply_text("唔比你入！")
        #                 return
        #         else:
        #             raise Exception
        # except:
        update.message.reply_text("吓。求其揾個command用下，撳 /help 睇點用。有咩事揾 @Trainer_Jono 。")


def bot_help(bot, update):
    try:
        update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25) (尚未完成)\n"
                                      "[Source code](https://www.codepile.net/pile/3aD3DPkD) (尚未更新)\n"
                                      "¯\\\_(ツ)\_/¯")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


@run_async
def tag9js(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    msg = update.message
    if msg.chat_id == -1001295361187:
        js_info = bot.get_chat_member(msg.chat_id, 190726372)
        if js_info.user.username:
            sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                                  reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]))
            sleep(15)
            msg.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
            sent.delete()
        else:
            msg.reply_text("Denied. User does not have a username.")
    elif update.message.chat_id < 0:
        update.message.reply_text("Denied. This group or supergroup is not allowed to use this command.")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
        update.message.reply_text("呢個指令只可以喺HK Duker用，歡迎撳下面個掣入嚟HK Duker一齊 /tag9js 。",
                                  reply_markup=reply_markup)


can_use_tag9 = (463998526, 487754154, 426072433, 49202743, 442517724, 190726372, 106665913)
# respectively  Tr. Jono,  Ms. Symbol, Giselle,   Siu Kei,  Chestnut,  JS,        Jeffffffc


@run_async
def tag9(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    msg = update.message
    if msg.from_user.id not in can_use_tag9:
        msg.reply_text("Denied. You are not authorized to use this command.")
    elif msg.chat_id > 0:
        msg.reply_text("You cannot tag people in a private chat with me.")
    elif msg.reply_to_message:
        tag9_part2(msg, bot.get_chat_member(msg.chat_id, msg.reply_to_message.from_user.id))
    elif not args:
        msg.reply_text("Please specify the user you would like to tag.")
    else:
        try:
            tag9_part2(msg, bot.get_chat_member(msg.chat_id, int(args[0])))
        except ValueError:
            msg.reply_text("Failed. Argument is not an integer.")
        except BadRequest:
            msg.reply_text("Failed. User has never joined this group or does not exist.")


@run_async
def tag9_part2(msg, u_info):
    if u_info.status in ("restricted", "left", "kicked"):
        msg.reply_text("Denied. User is either restricted or not in this group.)")
    elif u_info.user.id in (463998526, 506548905):
        msg.reply_text("Denied. User cannot be tagged.")
    elif u_info.user.is_bot:
        msg.reply_text("Denied. User is a bot.")
    elif u_info.user.username is None:
        msg.reply_markdown("Denied. User does not have a username.")
    else:
        sent = msg.reply_text("15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                              reply_markup=ReplyKeyboardMarkup([[u_info.user.name]]))
        sleep(15)
        msg.reply_text("Keyboard removed.", reply_markup=ReplyKeyboardRemove(), quote=False)
        try:
            sent.delete()
        except Exception:
            pass


def remove_keyboard(bot, update):
    if update.message.chat_id < 0:
        update.message.reply_text("Keyboard removed.", reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("no u")


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
    text = update.message.text
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
            bot.kick_chat_member(msg.chat_id, user.id)
        except Exception:
            pass
        try:
            update.message.delete()
        except Exception:
            pass


def general_responses(bot, update):
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
    elif msg:
        check_number_dude(bot, update, msg.from_user)
    elif msg.pinned_message:
        if user.id != 463998526:
            msg.reply_markdown(user.mention_markdown(user.full_name) + "又pin嘢...🙃", quote=False)
    elif msg.sticker:
        if msg.sticker.set_name in ("payize2", "FPbabydukeredition"):
            msg.reply_text("嘩屌又係bb，見到都反胃。")
    elif update.message.text:
        swear_word_detector(bot, update)
        text = update.message.text.lower()
        if text == "hello" and user.id == 463998526:
            msg.reply_text("主人你好！")
        if update.effective_user.id != 463998526 and msg.chat_id < 0 and "@trainer_jono" in text:
            update.message.reply_text("唔好tag我主人，乖。")
        if text == "js is very on9":
            update.message.reply_text("Your IQ is 500!")
        if "trainer jono is rubbish" in text:
            update.message.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")


def echo(bot, update):
    msg = update.message
    try:
        args = msg.text.split(" ", 1)[1]
        if msg.reply_to_message:
            try:
                msg.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
            except Exception as e:
                msg.reply_text("Markdown error: {}\nBy the way, the parse_mode is markdown. You can "
                               "use a backslash (\"\\\") before a markdown character to escape it.".format(str(e)))
            try:
                msg.delete()
            except:
                pass
        else:
            try:
                msg.reply_markdown(args, disable_web_page_preview=True, quote=False)
            except Exception as e:
                msg.reply_text("Markdown error: {}\nBy the way, the parse_mode is markdown. You can "
                               "use a backslash (\"\\\") before a markdown character to escape it.".format(str(e)))
            try:
                msg.delete()
            except:
                pass
    except IndexError:
        if update.message.reply_to_message:
            if msg.reply_to_message.text:
                try:
                    msg.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                   quote=False)
                except Exception as e:
                    msg.reply_text("Markdown error: {}\nBy the way, the parse_mode is markdown. You can "
                                   "use a backslash (\"\\\") before a markdown character to escape it.".format(str(e)))
                try:
                    msg.delete()
                except:
                    pass
            else:
                msg.reply_to_message.reply_text("No text in this message...🙃")
        else:
            msg.reply_text("""Deez r da waes:
            /r <text>
            /r [reply to a text message (files with captions don't count) not sent by other bots]
            /r <text> [reply to a message not sent by other bots]
            More info in /help.""")


# @run_async
# def echo3(bot, update):
#     try:
#         args = update.message.text.split(" ", 1)[1]
#         if update.message.reply_to_message:
#             for i in range(3):
#                 update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
#                 if i == 3:
#                     break
#                 sleep(1)
#         else:
#             for i in range(3):
#                 update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
#                 if i == 3:
#                     break
#                 sleep(1)
#     except IndexError:
#         try:
#             if update.message.reply_to_message:
#                 if update.message.reply_to_message.text:
#                     for i in range(3):
#                         update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
#                                                   quote=False)
#                         if i == 3:
#                             break
#                         sleep(1)
#                 else:
#                     update.message.reply_text("人地條訊息都唔係文字訊息...🙃")
#             else:
#                 update.message.reply_text("Dis is da wae: /r3 <text> and/or (reply to a message)\nMore info in /help.")
#         except Exception as e:
#             update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
#                                           .format(helpers.escape_markdown(str(e))))
#     except Exception as e:
#         update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
#                                       .format(helpers.escape_markdown(str(e))))


def user_info(bot, update):
        if update.message.reply_to_message:
            if update.message.chat_id < 0:
                user = update.message.reply_to_message.from_user
                if user.is_bot:
                    text = "*Information of this bot*"
                else:
                    text = "*Information of this user*"
                text += "\n\nUser id: `{}`\nFirst name: {}".format(user.id, helpers.escape_markdown(user.first_name))
                if user.last_name:
                    text += "\nLast name: {}".format(helpers.escape_markdown(user.last_name))
                    text += "\nFull name: {}".format(helpers.escape_markdown(user.full_name))
                if user.username:
                    text += "\nUsername: @{}".format(helpers.escape_markdown(user.username))
                if user.language_code:
                    text += "\nLanguage code: {}".format(user.language_code)
                try:
                    nub = bot.get_chat_member(update.message.chat_id, user.id)
                except BadRequest:
                    text += "\n\n*User has never joined {}*".format(update.effective_chat.title)
                    update.message.reply_text(text)
                    return
                if nub.status == "creator":
                    text += "\n\n*Creator* of {}".format(update.effective_chat.title)
                elif nub.status == "administrator":
                    text += "\n\n*Administrator* of {}".format(update.effective_chat.title)
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
                elif nub.status == "member":
                    text += "\n\n*Member* of {}".format(update.effective_chat.title)
                elif nub.status == "restricted":
                    text += "\n\n*Restricted* in {}*".format(update.effective_chat.title)
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
                elif nub.status == "left":
                    text += "\n\n*Left {}".format(update.effective_chat.title)
                elif nub.status == "kicked":
                    text += "\n\n*Banned* in {}".format(update.effective_chat.title)
                update.message.reply_markdown(text)
            else:
                update.message.reply_text("暫時群組先用到，pm就收皮先。")
        else:
            update.message.reply_text("Dis is da wae: /user_info [reply to a message]")


def get_id(bot, update):
    try:
        if update.message.reply_to_message:
            update.message.reply_markdown("佢嘅user id: ```{}```".format(update.message.reply_to_message.from_user.id))
        else:
            update.message.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```"
                                          .format(update.message.chat_id, update.effective_user.id))
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


def get_message_link(bot, update):
    try:
        if update.message.reply_to_message:
            group_info = bot.get_chat(update.message.chat_id)
            if group_info.type == "supergroup" and group_info.username:
                    update.message.reply_text("t.me/{}/{}".format(group_info.username,
                                                                  update.message.reply_to_message.message_id))
            else:
                update.message.reply_text("Public supergroup先用得架柒頭。")
        else:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


def get_file_id(bot, update):
    if update.message.reply_to_message:
        msg = update.message.reply_to_message
        if msg.audio:
            get_file_id_response(bot, update, "段音頻", msg.audio.file_id)
        elif msg.photo:
            get_file_id_response(bot, update, "張相", msg.photo[-1].file_id)
        elif msg.sticker:
            get_file_id_response(bot, update, "張貼紙", msg.sticker.file_id)
        elif msg.video:
            get_file_id_response(bot, update, "段影片", msg.video.file_id)
        elif msg.voice:
            get_file_id_response(bot, update, "段錄音", msg.voice.file_id)
        elif msg.video_note:
            get_file_id_response(bot, update, "段影片", msg.video_note.file_id)
        elif msg.document:
            get_file_id_response(bot, update, "份文件", msg.document.file_id)
        else:
            update.message.reply_text(get_file_id_error())
    else:
        update.message.reply_text(get_file_id_error())


def get_file_id_response(bot, update, file_type, file_id):
    update.message.reply_markdown("呢{}嘅file id: ```{}```".format(file_type, file_id))


def get_file_id_error():
    text = """Dis is da wae: /get_file_id [reply to message containing a supported file]
    Supported file types include:
    Audios (.mp3)
    Documents (general files)
    Photos (most image formats are supported)
    Stickers (.webp)
    Videos (.mp4)
    Voice recordings (.ogg)
    Video messages"""
    return text


def ping(bot, update):
    update.message.reply_markdown("Ping你老母？！")


def phantom_of_the_opera(bot, update):
    try:
        update.message.reply_audio("AwADBQADIgADsZ35Vf15qTeOTDR3Ag", quote=False)
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


def beefball_christ(bot, update):
    try:
        update.message.reply_audio("AwADBQADIwADsZ35VVzG9kRL3IU8Ag", quote=False)
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    token = "506548905:AAFCkZ5SI9INLEb0fwRHRlEji4Or6s8B9DQ"
    name = "on9bot"
    port = os.environ.get('PORT')
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9js", tag9js))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("file_id", get_file_id))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("x", phantom_of_the_opera))
    dp.add_handler(CommandHandler("r", echo))
#    dp.add_handler(CommandHandler("r3", echo3))
    dp.add_handler(CommandHandler("y", beefball_christ))
    dp.add_handler(CommandHandler("user_info", user_info))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, general_responses))
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(port), url_path=token, clean=True)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(name, token))
    updater.idle()


if __name__ == "__main__":
    main()
