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


# class Victim:
#     def __init__(self, name, user_id):
#         self.name = name
#         self.user_id = user_id
#         self.mention = "[{}](tg://user?id={})".format(name, user_id)
#         self.alive = True
#
#
# class Game:
#     def __init__(self, chat_id, msg):
#         self.chat_id = chat_id
#         self.game_state = "joining"
#         self.victims = []
#         self.msg = msg
#
#     def add_player(self, bot, update):
#         user = update.effective_user
#         victim_count = len(self.victims)
#         if not self.victims:
#             self.victims.append(Victim(user.full_name, user.id))
#             update.message.reply_text(ww_join_text)
#         elif victim_count < 4:
#             if user.id in [victim.id for victim in self.victims]:
#                 update.message.reply_text(ww_join_alr_text)
#             else:
#                 self.victims.append(Victim(user.full_name, user.id))
#                 update.message.reply_text(ww_join_text)
#                 self.send_to_group(bot, ww_join_gp_text.format(self.victims[-1].mention))
#                 if len(self.victims) == 4:
#                     bot.edit_message_text(self.msg.text, chat_id=self.msg.chat_id, message_id=self.message_id)
#                     self.start_trolling(bot)
#         else:
#             update.message.reply_text(ww_start_alr_text)
#
#     def send_to_group(self, bot, text):
#         bot.send_message(self.chat_id, text, parse_mode="Markdown")
#         sleep(1)
#
#     def send_victim_list(self, bot):
#         joined_victims_text = "在生玩家: {}/5\n".format(len([victim for victim in self.victims if victim.alive]))
#         for victim in self.victims:
#             if victim.alive:
#                 joined_victims_text += "\n{} - 在生".format(victim.mention)
#         joined_victims_text += "\n{} - 在生".format(on9bot_mention)
#         for victim in self.victims:
#             if not victim.alive:
#                 joined_victims_text += "\n{}廢村 - 死左".format(victim.mention)
#         return joined_victims_text
#
#     def send_victim_list_game_end(self, bot):
#         victim_list_game_end = "在生玩家: 1/5\n"
#         for victim in self.victims:
#             victim_list_game_end += "\n{}廢村 - 死左 輸".format(victim.mention)
#         victim_list_game_end += "\n{}村長兼槍手 - 在生 贏".format(on9bot_mention)
#         return victim_list_game_end
#
#     def start_trolling(self, bot):
#         self.send_to_group(bot, ww_on9bot_join_text)
#         self.send_to_group(bot, ww_first_night_text)
#         for victim in self.victims:
#             bot.send_message(victim.user_id, ww_role_text)
#         sleep(29)
#         self.send_to_group(bot, ww_shot.format(self.victims[0].mention))
#         sleep(89)
#         self.send_to_group(bot, ww_pre_reveal)
#         self.send_to_group(bot, ww_reveal.format(on9bot_mention))
#         self.send_to_group(bot, ww_lynch_decision.format(self.victims[1].mention))
#         self.send_to_group(bot, "The mayor has decided who to lynch. {0} is dead. {0} was a villager.\n\n"
#                                 "Night has fallen.  Everyone heads to bed, weary after another stressful day. "
#                                 "Night players: you have 30 seconds use your actions!")
#         sleep(29)
#         self.send_to_group(bot, ww_shot.format(self.victims[2].name))
#         self.send_to_group(bot, "Two players remain. {} grins, takes out his gun, aims at {} and shoots!"
#                            .format(on9bot_mention, self.victims[3].name))
#         self.send_to_group(bot, "槍手: \"頂！Para比得我兩粒子彈，無撚曬。不過我好似仲收埋左幾粒㗎喎，去鬼左邊...？*Reloads gun with bullets*")
#         self.send_to_group(bot, "{0} isn't stupid and immediately runs away from On9 Village! {0} was a villager."
#                            .format(self.victims[3].name))
#         self.send_to_group(bot, "槍手贏左！")
#         self.send_to_group(bot, self.send_victim_list_game_end(bot))
#         del running_ww_games[self.chat_id]


# WW Dialogues
# on9bot_mention = "[On9 Bot](tg://user?id=506548905)"
# ww_join_text = "你成功加入左游戲。"
# ww_join_alr_text = "好心你入左game咪再㩒掣啦。"
# ww_join_gp_text = "{}加入左游戲。"
# ww_on9bot_join_text = "唉，難得有四個人，-1開到game。喂，不如趁我得閒，等我入嚟玩殘你弟班柒頭，哈哈。"
# ww_start_alr_text = "開始左，撳乜撚掣？"
# ww_role_text = "你又係死廢村啦，真係好同情你。"
# ww_first_night_text = "開波！我pm左你地角色啦。各位柒頭，你地30秒做嘢。"
# ww_shot = "柒頭槍手琴日又飲醉左，殺撚左{0}，真係on9過本bot幾廿倍。{0}原來係廢村。\n\n"
# ww_pre_reveal = "夠鐘，各位柒頭有90秒投票殺—— 屌！好彩嚟得切。"
# ww_reveal = "{0}突然大嗌︰「嘈咩啊你地班柒頭！我係村長！」，轉個頭拎咗委任證出黎，由今晚起，{0}就係村長，每晚殺邊個都係佢話事" \
#             "，冇票比你班廢村投。"
# ww_lynch_decision = "我話殺{}!"


def start(bot, update):  # add args back later
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
        #             finally:
        #
        #         else:
        #             raise Exception
        # except:
        update.message.reply_text("吓。求其揾個command用下，撳 /help 睇點用。有咩事揾 @Trainer_Jono 。")


running_ww_games = {}


# def ww_start(bot, update):
#     chat_id = update.message.chat_id
#     user = update.effective_user
#     if chat_id > 0:
#         update.message.reply_text("群組先用到開到game喎。")
#         return
#     if running_ww_games.get(chat_id):
#         update.message.reply_text("你地已經玩梗就咪嘈啦。")
#     else:
#         join_url = "https://t.me/On9Bot?start=joinww_" + str(chat_id)
#         reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("撳我", url=join_url)]])
#         msg = update.message.reply_markdown("{0}開始左場狼人，撳掣入嚟玩啦！五個人先開到game。\n{0}，記得你都要撳掣先入到game。"
#                                       .format(user.mention_markdown(user.full_name)), reply_markup=reply_markup)
#         running_ww_games[chat_id] = Game(chat_id, msg)
#
#
# check if game exists in group
# if not, create a game


def bot_help(bot, update):
    try:
        update.message.reply_markdown("[On9Bot所有功能](http://telegra.ph/On9Bot-Help-03-25) (尚未完成)\n"
                                      "[Source code](https://www.codepile.net/pile/3aD3DPkD) (尚未更新)\n"
                                      "¯\\_(ツ)\_/¯")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
                update.message.reply_markdown("[JS](tg://user?id=190726372)del咗username，本bot愛莫能助")
        elif update.message.chat_id < 0:
            update.message.reply_markdown("呢個群組用唔到 /tag9js 㗎。")
        else:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("加入HK Duker", url="https://t.me/hkduker")]])
            update.message.reply_text("呢個指令只可以喺HK Duker用，歡迎撳下面個掣入嚟HK Duker一齊 /tag9js 。",
                                      reply_markup=reply_markup)
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


can_use_tag9 = (463998526, 487754154, 426072433, 49202743, 442517724, 190726372, 106665913)
# respectively   Tr. Jono, Ms. Symbol, Giselle,   Siu Kei,  Chestnut,  JS,        Jeffffffc


@run_async
def tag9(bot, update, args):
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        if update.effective_user.id in can_use_tag9:
            if update.message.chat_id > 0:
                update.message.reply_text("PM無得tag9人喎。")
                return
            if update.message.reply_to_message:
                    if update.message.reply_to_message.from_user.id == 463998526:
                        update.message.reply_text("Zzz... Waht?")
                        return
                    if update.message.reply_to_message.from_user.id == 506548905:
                        update.message.reply_text("Zzz... Waht?")
                        return
                    if update.message.reply_to_message.from_user.is_bot:
                        update.message.reply_text("Tag9 bot？咁無聊？")
                        return
                    user_info = bot.get_chat_member(update.message.chat_id,
                                                    update.message.reply_to_message.from_user.id)
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
                        update.message.reply_text("吓？人地唔喺呢度都要tag9？")
            else:
                try:
                    args = int(args[0])
                except (ValueError, IndexError):
                    update.message.reply_text("咁用先啱喎： /tag9 <user id>。你應該知道user id係咩掛。")
                    return
                except Exception as e:
                    update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人"
                                                  "[Trainer Jono](tg://user?id=463998526)。"
                                                  .format(helpers.escape_markdown(str(e))))
                    return
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
                        update.message.reply_text("Tag9 bot？咁無聊？")
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
                    update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人"
                                                  "[Trainer Jono](tg://user?id=463998526)。"
                                                  .format(helpers.escape_markdown(str(e))))
        else:
            update.message.reply_text("唔好亂用Trainer Jono嘅指令，乖。")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
                update.message.reply_markdown("Ding-a-ling-a-ling, ding-a-fucking-ling...\n"
                                              "電話又響啊...原來係[{}](tg://user?id={})又pin嘢...🙃"
                                              .format(update.message.from_user.full_name, update.message.from_user.id),
                                              quote=False)
        elif update.message.sticker:
            if update.message.sticker.set_name == "payize2" or update.message.sticker.set_name == "FPbabydukeredition":
                update.message.reply_text("嘩屌又係bb啊，媽咪我好驚驚！！！")
        elif update.message.text:
            swear_word_detector(bot, update)
            u = update.message.text.lower()
            if u == "hello" and update.effective_user.id == 463998526:
                update.message.reply_text("主人你好！")
            if update.effective_user.id != 463998526 and update.effective_chat.type in ("group", "supergroup") and "@trainer_jono" in u:
                update.message.reply_text("唔好tag我主人，乖。")
            if u == "js is very on9":
                update.message.reply_text("Your IQ is 500!")
            if "trainer jono is rubbish" in u:
                update.message.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
            update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                          .format(helpers.escape_markdown(str(e))))
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
    try:
        if update.message.reply_to_message:
            if update.effective_chat.type in ("supergroup", "group"):
                user = update.message.reply_to_message.from_user
                if user.is_bot:
                    text = "*Information of this bot*"
                else:
                    text = "*Information of this user*"
                text += "\n\nUser id: ```{}```\nFirst name: {}".format(user.id, helpers.escape_markdown(user.first_name))
                if user.last_name:
                    text += "\nLast name: {}".format(helpers.escape_markdown(user.last_name))
                    text += "\nFull name: {}".format(helpers.escape_markdown(user.full_name))
                if user.username:
                    text += "\nUsername: @{}".format(helpers.escape_markdown(user.username))
                if user.language_code:
                    text += "\nLanguage code: {}".format(user.language_code)
                try:
                    nub = bot.get_chat_member(update.message.chat_id, user.id)
                    if nub.status == "creator":
                        text += "\n\n*Creator* of {}".format(update.effective_chat.title)
                    elif nub.status == "administrator":
                        text += "\n\n*Administrator* of {}".format(update.effective_chat.title)
                    elif nub.status == "member":
                        text += "\n\n*Member* of {}".format(update.effective_chat.title)
                    elif nub.status == "restricted":
                        text += "\n\nUser has *restricted* rights but *may / may not* be a *member* of {}*"\
                            .format(update.effective_chat.title)
                    elif nub.status == "left":
                        text += "\n\nUser does *not* have *restricted* rights but is *not* a *member* in {}"\
                            .format(update.effective_chat.title)
                    elif nub.status == "kicked":
                        text += "*\n\nUser is banned in {}*".format(update.effective_chat.title)
                except BadRequest:
                    text += "\n\n*User has never joined {}*".format(update.effective_chat.title)
                    update.message.reply_text(text)
                except Exception as e:
                    update.message.reply_markdown(
                        "有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                        .format(helpers.escape_markdown(str(e))))
                finally:
                    if nub.status == "administrator":
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
                    if nub.status == "restricted":
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
                    update.message.reply_markdown(text)
            else:
                update.message.reply_text("This command is currently only available in groups and supergroups.")
        else:
            update.message.reply_text("Dis is da wae: /user_info [reply to a message]")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


def get_file_id_response(bot, update, file_type, file_id):
    update.message.reply_markdown("呢{}嘅file id: ```{}```".format(file_type, file_id))


def ping(bot, update):
    try:
        update.message.reply_markdown("Pong...?\n```0.001```\n\nSorry this took long to send but Telegram said I was "
                                      "too popular and wouldn't let me send messages for a bit...")
    except Exception as e:
        update.message.reply_markdown("有嘢出錯喎: {}\n唔明出咩錯或者覺得係bot有嘢出錯，歡迎你pm我主人[Trainer Jono](tg://user?id=463998526)。"
                                      .format(helpers.escape_markdown(str(e))))


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
