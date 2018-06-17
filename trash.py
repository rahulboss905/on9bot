# This file contains some code used before but not used now. Perhaps useful in the future? (Nein.)
# Most of them are db stuff.
#
# import psycopg2
# import datetime
#
# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#
# jeff_bday_text = "".join("""為咗慶祝Jeff生日，JS將會捐錢比 @werewolfbot 同 @Mud9bot。你亦可以支持兩個bot嘅發展，只要撳
# 下面個掣就可以提高JS捐額HK$1(係咪好多呢)。全部人同我撳撳撳撳撳...\n\n捐額暫時為HK${}""".split("\n", 1))
#
# HK_DUKER_ID = -1001295361187
#
#
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
#
#
# def jeff_bday_donate(bot, update):
#     query = update.callback_query
#     query.answer()
#     nub_id = query.from_user.id
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT amount FROM jeff_bday_donate WHERE user_id = %s", (nub_id,))
#         nub = cur.fetchone()
#         if not nub:
#             cur.execute("INSERT INTO jeff_bday_donate VALUES (%s, 1)", (nub_id,))
#         else:
#             cur.execute("UPDATE jeff_bday_donate SET amount = %s WHERE user_id = %s", (nub[0] + 1, nub_id))
#         conn.commit()
#     finally:
#         cur.close()
#
#
# @run_async
# def jeff_bday_edit_msg_wait(bot, job):
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT amount FROM jeff_bday_donate")
#         amounts = cur.fetchall()
#         cur.execute("SELECT msg_id FROM jeff_bday_temp")
#         msg_id = cur.fetchone()[0]
#     finally:
#         cur.close()
#     total = sum([a[0] for a in amounts])
#     reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Add HK$1", callback_data="donate")]])
#     try:
#         bot.edit_message_text(jeff_bday_text.format(total), HK_DUKER_ID, msg_id, reply_markup=reply_markup)
#     except TelegramError as e:
#         pass
#
#
# def jeff_bday_end(bot, job):
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT amount FROM jeff_bday_donate")
#         amounts = cur.fetchall()
#         cur.execute("SELECT msg_id FROM jeff_bday_temp")
#         msg_id = cur.fetchone()[0]
#     finally:
#         cur.close()
#     bot.edit_reply_markup(chat_id=HK_DUKER_ID, message_id=msg_id)
#     total = sum([a[0] for a in amounts])
#     bot.send_message(-1001295361187, "活動完結！Jeff會收到JS HK${}嘅捐款。".format(total))
#     job.job_queue.stop()
#
#
# def sql(bot, update):
#     msg = update.effective_message
#     if msg.from_user.id != 463998526:
#         msg.reply_text("no u")
#         return
#     else:
#         cur = conn.cursor()
#         try:
#             query = msg.text.split(" ", 1)[1]
#         except IndexError:
#             msg.reply_text("no u")
#             return
#         try:
#             cur.execute(query)
#             try:
#                 output = cur.fetchall()
#             except Exception:
#                 output = None
#             conn.commit()
#             if output:
#                 msg.reply_markdown(escape_markdown(str(output)))
#             else:
#                 msg.reply_markdown("Success! No output was returned.")
#         except Exception as e:
#             msg.reply_markdown(f"An error occured: `{escape_markdown(str(e))}`")
#         finally:
#             cur.close()
#
#
# INIT_DB_SQL = """CREATE TABLE IF NOT EXISTS jeff_bday_donate (user_id BIGINT UNIQUE NOT NULL, amount BIGINT NOT NULL);
# CREATE TABLE IF NOT EXISTS jeff_bday_temp (msg_id BIGINT NOT NULL);"""
#
#
# def main():
#     cur = conn.cursor()
#     try:
#         cur.execute(INIT_DB_SQL)
#         conn.commit()
#     finally:
#         cur.close()
#     dp.add_handler(CallbackQueryHandler(jeff_bday_donate))
#     dp.add_handler(CommandHandler("sql", sql, allow_edited=True))
#     job_queue = updater.job_queue
#     job_queue.run_repeating(jeff_bday_edit_msg_wait, 4)
#     job_queue.run_once(jeff_bday_end, datetime.datetime(2018, 6, 12, 0, 0, 0))
