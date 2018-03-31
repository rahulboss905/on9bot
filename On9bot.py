# On9Bot (an annoying Cantonese Telegram bot) source code
# Uses Python 3 and the python-telegram-bot library, hosted on Heroku

from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest
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


def start(bot, update):
    if update.message.chat_id > 0:
        update.message.reply_markdown("你好，我係全部Telegram bot之中最On9嘅，有邊個bot想同我鬥on9嘅可以同我主人"
                                      "[Trainer Jono](tg://user?id=463998526)講。撳 /help 睇點用。Zzz...",
                                      disable_web_page_preview=True)


def bot_help(bot, update):
    update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25)(尚未完成)\n"
                                  "[Source code](https://www.codepile.net/pile/3aD3DPkD)(尚未更新)\n"
                                  "¯\_(ツ)_/¯")


def tag9js_text():
    text = """限時十五秒，一齊撳掣tag死[JS](tg://user?id=190726372)啦！
五秒唔好撳個掣多過七次，如果唔係GH Bot會話你flood，mute左你，到時本bot幫你唔到㗎。
你可以隨時撳 /remove\_keyboard 整走個鍵盤。"""
    return text


@run_async
def tag9js(bot, update):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if update.message.chat_id == -1001295361187:
            js_info = bot.get_chat_member(-1001295361187, 190726372)
            if js_info.status != "creator":
                update.message.reply_markdown("一齊撳掣tag死——吓？！[JS](tg://user?id=190726372)去左邊？？？")
                return
            if js_info.user.username:
                update.message.reply_markdown(tag9js_text(),
                                              reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]),
                                              disable_web_page_preview=True)
                sleep(15)
                update.message.reply_text("我已經整走咗個鍵盤啦。",
                                          reply_markup=ReplyKeyboardRemove(), quote=False)
            else:
                update.message.reply_text("[JS](tg://user?id=190726372)del咗username？！豈有此理，等本大爺親自tag你啦！")
                for i in range(3):
                    update.message.reply_markdown("[JS](tg://user?id=190726372)！", quote=False)
                    sleep(2)
                update.message.reply_text("算啦，再tag JS我會攰死，今次放過佢啦。", quote=False)
        elif update.message.chat_id < 0:
            update.message.reply_markdown("呢個群組用唔到 /tag9js 㗎。")
        else:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
            update.message.reply_text("呢個指令只可以喺HK Duker用，歡迎撳下面個掣入嚟HK Duker一齊 /tag9js 。",
                                      reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


@run_async
def tag9(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if update.effective_user.id == 463998526 or (update.effective_user.id == 190726372 and
                                                     update.message.chat_id == -1001295361187):
            if update.message.chat_id > 0:
                update.message.reply_text("PM無得tag9人喎。")
                return
            if update.message.reply_to_message:
                try:
                    if update.message.reply_to_message.from_user.id == 463998526:
                        update.message.reply_text("我我——我好似突然之間盲咗，睇睇——睇唔到你條訊息喎。")
                        return
                    if update.message.reply_to_message.from_user.id == 506548905:
                        update.message.reply_text("我我——我好似突然之間盲咗，睇睇——睇唔到你條訊息喎。")
                        return
                    if update.message.reply_to_message.from_user.is_bot:
                        update.message.reply_text("Tag9 bot？咁無聊？")
                        return
                    user_info = bot.get_chat_member(update.message.chat_id,
                                                    update.message.reply_to_message.from_user.id)
                    if user_info.status == "restricted":
                        if not user_info.status.can_send_messages:
                            update.message.reply_text("吓？人地無得講嘢都要tag9？")
                            return
                    if user_info.status in ("administrator", "creator", "member", "restricted"):
                        if user_info.user.username:
                            update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                                          reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                            sleep(15)
                            update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
                        else:
                            update.message.reply_markdown("Tag唔到，佢無username。我tag一下lor。喂啊[{}](tg://user?id={})"
                                                          "。".format(user_info.full_name,user_info.user.id))
                    else:
                        update.message.reply_text("吓？人地唔喺呢個群組都要tag9？")
                except Exception as e:
                    update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                                  .format(str(e)))
            else:
                try:
                    args = int(args[0])
                except (ValueError, IndexError):
                    update.message.reply_text("咁用先啱喎： /tag9 <user id>。你應該知道user id係咩掛。")
                except Exception as e:
                    update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                                  .format(str(e)))
                if args == 463998526:
                    update.message.reply_text("我我——我好似突然之間盲咗，睇睇——睇唔到你條訊息喎。")
                    return
                if args == 506548905:
                    update.message.reply_text("我我——我好似突然之間盲咗，睇睇——睇唔到你條訊息喎。")
                if args <= 0:
                    update.message.reply_text("我又唔至於柒到唔知user id係正整數嘅。Zzz...")
                    return
                try:
                    user_info = bot.get_chat_member(update.message.chat_id, args)
                    if user_info.user.is_bot:
                        update.message.reply_text("Tag乜撚bot啊？")
                        return
                    if user_info.status == "restricted":
                        if not user_info.status.can_send_messages:
                            update.message.reply_text("吓？人地無得講嘢都要tag9？")
                    if user_info.status in ("administrator", "creator", "member"):
                        if user_info.user.username:
                            update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                                          reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                            sleep(15)
                            update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
                        else:
                            update.message.reply_markdown("Tag唔到，佢無username。我tag一下lor。"
                                                          "[柒頭](tg://user?id={})。".format(user_info.user.id))
                    else:
                        update.message.reply_text("吓？人地唔喺呢個群組都要tag9？")
                except BadRequest:
                    update.message.reply_text("乜呢個群組有呢個人咩？定Telegram入面根本無呢個人？定係啲數字亂打嘅？Zzz...")
                except Exception as e:
                    update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                                  .format(str(e)))
        else:
            update.message.reply_text("唔好亂用Trainer Jono嘅指令，乖。")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


# Ah, how boring it is after writing such a damn large function. raise BoredError("¯\_(ツ)_/¯")
# I wouldn't mind some drawings here, you know.
#   ____                       ____
#  |    \                     |    \                    |
#  |     \ ____ _____ ____    |     \ ____ ____ .  ____ |
#  |     | |  | | | | |  |    |     | |  | |  | | |___| |
#  |_____/ \_/\ | | | |  |    |_____/ \_/\ |  | | |___  |
#
#  _____ ____    ____
#    |  |       |                 |  /
#    |  |____   |____         ___ |/   ____
#    |      |       | |   |  |    |\  |____
# \__|  ____|   ____| |___|\ |___ | \ ____|


def remove_keyboard(bot, update):
    try:
        if update.message.chat_id < 0:
            update.message.reply_text("我已經整走咗個鍵盤啦（如有）。", reply_markup=ReplyKeyboardRemove())
        else:
            update.message.reply_text("我唔會整鍵盤比你撳，移乜除姐。")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


# YOU ARE ADVISED TO IGNORE THE FOLLOWING OFFENSIVE WORDS.
# THESE WORDS ARE ONLY FOR DETECTING OFFENSIVE WORDS IN TELEGRAM MESSAGES
# AND NOT INSULTING USERS OR OTHER PEOPLE.


cn_swear_words = ("屌", "閪", "柒", "撚", "鳩", "𨳒", "屄", "𨶙", "𨳊", "㞗", "𨳍", "杘")
cn_swear_words_in_eng = ("diu", "dllm", "dnlm", "diuneinomo", "diuneilomo")
eng_swear_words = ("anus", "arse", "ass", "axwound", "bampot", "bastard", "beaner", "bitch", "blowjob", "bollocks",
                   "bollox", "boner", "butt", "camaltoe", "carpetmuncher", "chesticle", "chinc", "chink", "choad",
                   "chode", "clit", "cock", "coochie", "choochy", "coon", "cooter", "cracker", "cum", "cunnie",
                   "cunnilingus", "cunt", "dago", "damn", "deggo", "dick", "dike", "dildo", "doochbag", "dookie",
                   "douche", "dumb", "dyke", "fag", "fellatio", "feltch", "flamer", "fuck", "fidgepacker", "gay",
                   "goddamn", "goddamnit", "gooch", "gook", "gringo", "guido", "handjob", "hardon", "heeb", "hell",
                   "hoe", "homo", "honkey", "humping", "jagoff", "jap", "jerk", "jigaboo", "jizz", "junglebunny",
                   "kike", "kooch", "kootch", "kraut", "kunt", "kyke", "lesbian", "lesbo", "lezzie", "mick", "minge",
                   "muff", "munging", "negro", "nigaboo", "nigga", "nigger", "niglet", "nutsack", "paki", "panooch",
                   "pecker", "penis", "piss", "polesmoker", "pollock", "poon", "porchmonkey", "prick", "punanny",
                   "punta", "pussy", "pussies", "puto", "queef", "queer", "renob", "rimjob", "ruski", "schlong",
                   "scrote", "shit", "shiz", "skank", "skeet", "slut", "smeg", "snatch", "spic", "splooge", "spook",
                   "tard", "thot", "testicle", "tit", "twat", "vajj", "vag", "vajayjay", "vjayjay", "wank", "wetback",
                   "whore", "wop", "wtf", "fk", "asshole", "bullshit", "shitty", "asshole")


def cn_swear_word_detector():
    for cn_swear_word in cn_swear_words:
        if cn_swear_word in t:
            return True


def cn_swear_word_in_eng_detector():
    for cn_swear_word_in_eng in cn_swear_words_in_eng:
        for word in t:
            if word == cn_swear_word_in_eng:
                return True


def eng_swear_word_detector():
    for eng_swear_word in eng_swear_words:
        for word in t:
            if word == eng_swear_word:
                return True


def swear_word_detector(bot, update):
    try:
        if update.message.text:
            global t
            t = update.message.text
            if cn_swear_word_detector():
                if update.message.chat_id < 0:
                    update.message.reply_text("講粗口？！記你一次大過！")
                else:
                    update.message.reply_text("PM講粗口姐，我先懶得理你。Zzz...")
                return
            t = t.lower().split(" ")
            if cn_swear_word_in_eng_detector() or eng_swear_word_detector():
                if update.message.chat_id < 0:
                    update.message.reply_text("講粗口？！記你一次大過！")
                else:
                    update.message.reply_text("PM講粗口姐，我先懶得理你。Zzz...")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


# maybe change to be use handler and groups


def general_responses(bot, update):
    try:
        if update.message.new_chat_members:
            for on9user in update.message.new_chat_members:
                if on9user.id == 506548905:
                    update.message.reply_text("嘩，邊撚到嚟㗎？")
                    update.message.reply_text("你好，我係全部Telegram bot之中最On9嘅，有邊個bot想同我鬥on9嘅可以同我主人"
                                              "[Trainer Jono](tg://user?id=463998526)講。撳 /help 睇點用。Zzz...")
                elif match(r'\d\d\d\d\d\d\d\d', on9user.first_name):
                    if match(r'\d\d\d\d\d\d\d\d', on9user.last_name):
                        update.message.reply_text("又係數字人？我屌！我ban 9佢啦。")
                        bot.kick_chat_member(update.message.chat_id, on9user.id)
                elif on9user.is_bot:
                    update.message.reply_text("Zzz...哦？新bot喎，乜水？")
        elif update.message.left_chat_member:
            update.message.reply_text(update.message.left_chat_member.full_name + "離開左群組...")
        elif match(r'\d\d\d\d\d\d\d\d', update.message.from_user.first_name) and match(r'\d\d\d\d\d\d\d\d', update.from_user.last_name):
            update.message.reply_text("又係數字人？我屌！我ban 9數字人啦。", quote=False)
            update.message.delete()
            bot.kick_chat_member(update.message.chat_id, update.message.from_user.id)
        elif update.message.pinned_message:
            if update.message.from_user.id != 463998526:
                update.message.reply_markdown("Zzz...電話又響啊...原來係[{}](tg://user?id={})又pin嘢...🙃".format(
                    update.message.from_user.full_name,update.message.from_user.id), quote=False)
        elif update.message.sticker:
            if update.message.sticker.set_name == "payize2" or update.message.sticker.set_name == "FPbabydukeredition":
                update.message.reply_text("嘩屌又係bb啊媽咪我好驚驚")
        elif update.message.text:
            swear_word_detector(bot, update)
            u = update.message.text.lower()
            if u == "hello" and update.effective_user.id == 463998526:
                update.message.reply_text("主人你好！")
            if update.effective_user.id != 463998526 and update.effective_chat.type in ("group", "supergroup") and "@trainer_jono" in u:
                update.message.reply_text("唔好tag我主人，乖。")
            if u == "js is very on9":
                update.message.reply_text("Your IQ is 500")
            if "trainer jono is rubbish" in u:
                update.message.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


def echo(bot, update):
    try:
        args = update.message.text.split(" ", 1)[1]
        if update.message.reply_to_message:
            update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
            update.message.delete()
        else:
            update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
            update.message.delete()
    except IndexError:
        try:
            if update.message.reply_to_message:
                if update.message.reply_to_message.text:
                    update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                              quote=False)
                    update.message.delete()
                else:
                    update.message.reply_text("人地條訊息都唔係文字訊息...🙃")
            else:
                update.message.reply_text("Dis is da wae: /r <text> and/or (reply to a message)\nMore info in /help.")
        except Exception as e:
            update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                          .format(str(e)))
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


# fix to use args = update.message.text.split(" ", 1)[1]

@run_async
def echo3(bot, update):
    try:
        args = update.message.text.split(" ", 1)[1]
        if update.message.reply_to_message:
            for i in range(3):
                update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
                if i == 3:
                    break
                sleep(1)
        else:
            for i in range(3):
                update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
                if i == 3:
                    break
                sleep(1)
    except IndexError:
        try:
            if update.message.reply_to_message:
                if update.message.reply_to_message.text:
                    for i in range(3):
                        update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                                  quote=False)
                        if i == 3:
                            break
                        sleep(1)
                else:
                    update.message.reply_text("人地條訊息都唔係文字訊息...🙃")
            else:
                update.message.reply_text("Dis is da wae: /r3 <text> and/or (reply to a message)\nMore info in /help.")
        except Exception as e:
            update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                          .format(str(e)))
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


# change to show all ChatMember and User info


def user_info(bot, update):
    try:
        if update.message.reply_to_message:
            if update.effective_chat.type in ("supergroup", "group"):
                user = update.message.reply_to_message.from_user
                if user.is_bot:
                    text = "*Information of this bot*"
                else:
                    text = "*Information of this user*"
                text += "\n\nUser id: {}\nFirst name: {}".format(user.id, user.first_name)
                if user.last_name:
                    text += "\nLast name: {}".format(user.last_name)
                    text += "\nFull name: {}".format(user.full_name)
                if user.username:
                    text += "\nUsername: {}".format(user.username)
                if user.language_code:
                    text += "\nLanguage code: {}".format(user.language_code)
                user = bot.get_chat_member(user.id, update.effective_chat)
                text += "\n\nUser's status in this {}: {}".format(update.effective_chat.type, user.status)
                if user.status == "creator":
                    update.message.reply_markdown(text)
                    return
                if user.status == "administrator":
                    if user.can_change_info:
                        text += "\nCan change group info: Yes"
                    else:
                        text += "\nCan change group info: No"
                    if user.can_delete_messages:
                        text += "\nCan delete messages: Yes"
                    else:
                        text += "\nCan delete messages: No"
                    if user.can_restrict_members:
                        text += "\nCan restrict, ban and unban members: Yes"
                    else:
                        text += "\nCan restrict, ban and unban members: No"
                    if user.can_pin_messages:
                        text += "\nCan pin messages: Yes"
                    else:
                        text += "\nCan pin messages: No"
                    if user.can_promote_members:
                        text += "\nCan add new admins: Yes"
                    else:
                        text += "\nCan add new admins: No"
                if user.status in ("administrator", "member"):
                    if user.can_send_messages:
                        text += "\n\nCan send messages: Yes"
                        if user.can_send_media_messages:
                            text += "\nCan send media: Yes"
                            if user.can_send_other_messages:
                                text += "\nCan send stickers and GIFs: Yes"
                            else:
                                text += "\nCan send stickers and GIFs: No"
                            if user.add_send_web_page_previews:
                                text += "\nCan send web page previews: Yes"
                            else:
                                text += "\nCan send web page previews: No"
                        else:
                            text += "\nCan send media: No"
                    else:
                        text += "\n\nCan send messages: No"
                update.message.reply_text(text)
            else:
                update.message.reply_text("This command is currently only available in groups and supergroups.")
        else:
            update.message.reply_text("Please reply to a message while using this command.")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


def get_id(bot, update):
    try:
        if update.message.reply_to_message:
            update.message.reply_markdown("佢嘅user id: ```{}```".format(update.message.reply_to_message.from_user.id))
        else:
            update.message.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```"
                                          .format(update.message.chat_id, update.effective_user.id))
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


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
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


def get_file_id(bot, update):
    try:
        if update.message.reply_to_message:
            x = update.message.reply_to_message
            if x.audio:
                get_file_id_response(bot, update, "段音頻", x.audio.file_id)
            elif x.photo:
                get_file_id_response(bot, update, "張相", x.photo[-1].file_id)
            elif x.sticker:
                get_file_id_response(bot, update, "張貼紙", x.sticker.file_id)
            elif x.video:
                get_file_id_response(bot, update, "段影片", x.video.file_id)
            elif x.voice:
                get_file_id_response(bot, update, "段錄音", x.voice.file_id)
            elif x.video_note:
                get_file_id_response(bot, update, "段影片", x.video_note.file_id)
            elif x.document:
                get_file_id_response(bot, update, "份文件", x.document.file_id)
            else:
                update.message.reply_text("Dis is da wae: /get_file_id [reply to message containing a supported file]\n"
                                          "Supported file types include audios (.mp3), documents (general files), "
                                          "photos (most image formats are supported), stickers (.webp), videos (.mp4), "
                                          "voice recordings (.ogg) and video messages.")
        else:
            update.message.reply_text("Dis is da wae: /get_file_id [reply to message containing a supported file]\n"
                                      "Supported file types include audios (.mp3), documents (general files), "
                                      "photos (most image formats are supported), stickers (.webp), videos (.mp4), "
                                      "voice recordings (.ogg) and video messages.")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)"
                                      .format(str(e)))


def get_file_id_response(bot, update, file_type, file_id):
    update.message.reply_markdown("呢{}嘅file id: ```{}```".format(file_type, file_id))


def ping(bot, update):
    try:
        update.message.reply_markdown("Pong...?\n```0.001```\n\nSorry this took long to send but Telegram said I was "
                                      "too popular and wouldn't let me send messages for a bit...")
    except Exception as e:
        update.message.reply_text(str(e))


# maybe change the two commands below to voice

def phantom_of_the_opera(bot, update):
    try:
        update.message.reply_audio("AwADBQADIgADsZ35Vf15qTeOTDR3Ag", quote=False)
    except Exception as e:
        update.message.reply_text(str(e))


def beefball_christ(bot, update):
    try:
        update.message.reply_audio("AwADBQADIwADsZ35VVzG9kRL3IU8Ag", quote=False)
    except Exception as e:
        update.message.reply_text(str(e))


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
    dp.add_handler(CommandHandler("r3", echo3))
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
