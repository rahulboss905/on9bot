#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ChatAction, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from telegram.error import BadRequest
from time import sleep
import logging
import re
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_markdown("我係全Telegram最On9嘅bot。有咩事可以揾我主人[Trainer Jono](tg://user?id=463998526)。")


def bot_help(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25)")


def tag9js_text():
    text = '''一齊撳掣tag死[JS](tg://user?id=190726372)啦！限時15秒，現在開始！JS受死啦！
呢個群組個Enforcer好鬼煩，flood小小就會踢走你。你要注意下，五秒唔好撳個掣多過七次，否則你會被踢走。
萬一你唔小心撳掣太快，比Grey Wolf Enforcer踢走左去火星，你可以global search [HK Duker](t.me/hkduker) 即刻入返嚟繼續撳掣tag JS。
你可以隨時撳 /remove\_keyboard 整走個keyboard。'''
    return text


@run_async
def tag9js(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if update.message.chat_id == -1001295361187:
        js_info = bot.get_chat_member(-1001295361187, 190726372)
        if js_info.user.username:
            update.message.reply_markdown(tag9js_text(),
                                          reply_markup=ReplyKeyboardMarkup([[js_info.user.name]]),
                                          disable_web_page_preview=True)
            sleep(15)
            update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
        else:
            update.message.reply_text("你條死JS，del咗username？！豈有此理，等本大爺親自tag你啦！")
            for i in range(0, 3):
                update.message.reply_markdown("[JS](tg://user?id=190726372)上水啦！", quote=False)
                sleep(2)
            update.message.reply_text("算啦，再tag JS我會攰死，今次放過你啦唉。", quote=False)
    elif update.message.chat_id < 0:
        update.message.reply_markdown("為咗減少對[JS](tg://user?id=190726372)嘅騷擾，呢個指令本群組用唔到㗎。")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
        update.message.reply_text("呢個指令只可以喺HK Duker用到，歡迎撳下面個掣入嚟HK Duker一齊tag死JS。",
                                  reply_markup=reply_markup)


@run_async
def tag9(bot, update, args):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    if update.effective_user.id != 463998526 and (update.effective_user.id != 190726372 and
                                                  update.message.chat_id != -1001295361187):
        update.message.reply_text("咪亂用Trainer Jono專用嘅指令啦。")
        return
    if update.message.chat_id > 0:
        update.message.reply_text("PM點tag9人姐？")
        return
    if update.message.reply_to_message:
        try:
            user_info = bot.get_chat_member(update.message.chat_id, update.message.reply_to_message.from_user.id)
            if user_info.user.username:
                update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                              reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                sleep(15)
                update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
            else:
                update.message.reply_markdown("Tag唔到，佢無username。我tag lor。[7](tg://user?id={})".format(user_info.user.id))
        except BadRequest:
            update.message.reply_text("呢個群組有呢個人咩？定根本無呢個人？Zzz...")
    else:
        try:
            args = int(args[0])
            if args == "":
                raise ValueError
        except ValueError:
            update.message.reply_text("打錯嘢喎。咁用先啱： /tag9 <user id>。 唔知user id係咩就死開。Zzz...")
            return
        try:
            user_info = bot.get_chat_member(update.message.chat_id, args)
            if user_info.user.username:
                update.message.reply_markdown("限時十五秒，唔好tag得太過分。",
                                              reply_markup=ReplyKeyboardMarkup([[user_info.user.name]]))
                sleep(15)
                update.message.reply_text("我已經整走咗個鍵盤啦。", reply_markup=ReplyKeyboardRemove(), quote=False)
            else:
                update.message.reply_text("Tag唔到，佢無username。")
        except BadRequest:
            update.message.reply_text("呢個群組有呢個人咩？定根本無呢個人？Zzz...")


def remove_keyboard(bot, update):
    if update.message.chat_id < 0:  # if this chat is a group
        update.message.reply_text("我已經整走咗個鍵盤啦（如有）。", reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text("我唔會整鍵盤比你撳，移乜除姐。")


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
                   "whore", "wop", "wtf", "fk", "asshole")


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
    global t
    t = update.message.text
    if cn_swear_word_detector():
        if update.message.chat_id < 0:
            update.message.reply_text("豈有此理，講粗口？！我最撚憎人講粗口，扣你一分操行分！")
            return
        else:
            update.message.reply_text("PM講粗口姐，我先懶得理你。")
            return
    t = t.lower().split(" ")
    if cn_swear_word_in_eng_detector():
        if update.message.chat_id < 0:
            update.message.reply_text("廣東話粗口嘅英文縮寫我睇得明㗎。我最撚憎人講粗口，扣你一分操行分！")
        else:
            update.message.reply_text("PM講粗口姐，我先懶得理你。")
    elif eng_swear_word_detector():
        if update.message.chat_id < 0:
            update.message.reply_text("I understand English swear words, noob. How dare you use swear words?! "
                                      "One conduct mark deducted!")
        else:
            update.message.reply_text("It's pm, no one cares if you swear.")
    else:
        return


def text_responses(bot, update):
    if update.message.new_chat_members:
        for on9user in update.message.new_chat_members:
            if re.match(r'\d\d\d\d\d\d\d\d', on9user.first_name):
                if re.match(r'\d\d\d\d\d\d\d\d', on9user.last_name):
                    update.message.reply_text("又係數字人？我屌！我ban 9數字人啦。")
                    bot.kick_chat_member(update.message.chat_id, on9user.id)
                    return
    y = update.message.from_user
    if re.match(r'\d\d\d\d\d\d\d\d', y.first_name):
        if re.match(r'\d\d\d\d\d\d\d\d', y.last_name):
            update.message.reply_text("又係數字人？我屌！我ban 9數字人啦。", quote=False)
            update.message.delete()
            bot.kick_chat_member(update.message.chat_id, update.message.from_user.id)
            return
    if update.message.pinned_message:
        if update.message.from_user.id == 463998526:
            update.message.reply_text("Trainer Jono pin嘢啊，係咪有人有意見？")
        else:
            update.message.reply_text("屌你老母咩 " + update.message.from_user.name + " ，pin嘢嘈醒全谷人。")
    if update.message.sticker:
        if update.message.sticker.set_name == "payize2" or update.message.sticker.set_name == "FPbabydukeredition":
            update.message.reply_text("屌你老母，Send乜撚bb啊，阻住個地球轉。")
    u = update.message.text.lower()
    if update.effective_user.id == 463998526:
        if u == "hello":
            update.message.reply_text("主人你好！")
        if u == "good dog":
            update.message.reply_text("屌你老母")
    if u == "trainer jono is rubbish":
        update.message.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg",
                                   caption="車娜 Jono is a wubbish. Tot肚ly wubbish. Dammit.")
    if "cough" in u:
        update.message.reply_text("Do you need some cough medicine?")
    if u == "js is very on9":
        update.message.reply_text("Your IQ is 500")


def echo(bot, update, args):
    args = " ".join(args)
    if update.message.reply_to_message:
        try:
            if args == "":
                update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                          quote=False)
                update.message.delete()
                return
            update.message.delete()
            update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)

        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
    else:
        try:
            if args == "":
                raise ValueError
            update.message.delete()
            update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")


def echo3(bot, update, args):
    args = " ".join(args)
    if update.message.reply_to_message:
        try:
            if args == "":
                for i in range(0, 3):
                    update.message.reply_text(update.message.reply_to_message.text, disable_web_page_preview=True,
                                              quote=False)
                return
            for i in range(0, 3):
                update.message.reply_to_message.reply_markdown(args, disable_web_page_preview=True)
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")
    else:
        try:
            if args == "":
                raise ValueError
            for i in range(0, 3):
                update.message.reply_markdown(args, disable_web_page_preview=True, quote=False)
        except ValueError:
            update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")


def get_id(bot, update):
    if update.message.reply_to_message:
        update.message.reply_markdown("佢嘅user id: ```{}```".format(update.message.reply_to_message.from_user.id))
    else:
        update.message.reply_markdown("呢個對話嘅chat id: ```{}```\n你嘅user id: ```{}```"
                                      .format(update.message.chat_id, update.effective_user.id))


def get_message_link(bot, update):
    if update.message.reply_to_message:
        group_info = bot.get_chat(update.message.chat_id)
        if group_info.type == "supergroup":
            if group_info.username:
                update.message.reply_text("t.me/{}/{}".format(group_info.username,
                                                              update.message.reply_to_message.message_id))
            else:
                update.message.reply_text("Public supergroup先用得架柒頭。")
        else:
            update.message.reply_text("Public supergroup先用得架柒頭。")
    else:
        update.message.reply_text("唔識用就咪撚用啦柒頭，睇 /help 啦。")


def get_audio_id(bot, update):
    if update.message.reply_to_message:
        if update.message.reply_to_message.audio:
            update.message.reply_markdown("File id for this audio file: ```{}```".format(update.message.reply_to_message.audio.file_id))
        else:
            update.message.reply_text("唔係audio file(.mp3)就收皮啦。")
    else:
        update.message.reply_text("覆住個audio file(.mp3)嚟用啦大佬。")


def get_voice_id(bot, update):
    if update.message.reply_to_message:
        if update.message.reply_to_message.voice:
            update.message.reply_markdown("File id for this voice file: ```{}```".format(update.message.reply_to_message.voice.file_id))
        else:
            update.message.reply_text("唔係voice file(.ogg)就收皮啦。")
    else:
        update.message.reply_text("覆住個voice file(.ogg)嚟用啦大佬。")


def ping(bot, update):
    update.message.reply_text("收到要屌你老母需時: 00:00.01\n999 MAX IN | 1 MAX OUT\n屌你老母需時︰00:00.01\n\n"
                              "Sorry this took long to send but Telegram said I was too popular and wouldn't let me "
                              "send messages for a bit...")


def poto(bot, update):
    update.message.reply_audio()


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    TOKEN = "506548905:AAH2pKTKJKjQ2RPh8ysEqyNNYQ-oQGKDkK0"
    NAME = "on9bot"
    PORT = os.environ.get('PORT')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", bot_help))
    dp.add_handler(CommandHandler("tag9js", tag9js))
    dp.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    dp.add_handler(CommandHandler("id", get_id))
    dp.add_handler(CommandHandler("link", get_message_link))
    dp.add_handler(CommandHandler("audio_id", get_audio_id))
    dp.add_handler(CommandHandler("voice_id", get_voice_id))
    dp.add_handler(CommandHandler("ping", ping))
    dp.add_handler(CommandHandler("tag9", tag9, pass_args=True))
    dp.add_handler(CommandHandler("r", echo, pass_args=True))
    dp.add_handler(CommandHandler("r3", echo3, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, swear_word_detector))
    dp.add_handler(MessageHandler(Filters.all, text_responses), group=1)
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN, clean=True)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
