# import random
# from typing import List, Tuple, Union
#
# from telegram import Bot, Update
# from telegram.error import TelegramError
#
#
# def separator(args: str) -> List[str]:
#     sep = ", "
#     if "\n," in args:
#         sep = "\n,"
#         sep_args = args.split(",\n")
#     elif "\n" in args:
#         sep = "\n"
#         sep_args = args.split("\n")
#     elif "," in args:
#         sep_args = args.split(",")
#     else:
#         sep_args = args.split()
#     return [s.strip() for s in sep_args if not s.isspace()]
#
#
# def choice(bot: Bot, update: Update, num: Union[int, bool] = False) -> None:
#     try:
#         args = update.message.text.split(max_split=2)[0]
#     except IndexError:
#         if num:
#             update.message.reply_text(f"`{random.randint(1, num)}`")
#         else:
#             update.message.reply_text(random.choice(("Heads", "Tails")))
#     else:
#         random_choice = random.choice(separator(args)[0])
#         try:
#             update.message.reply_markdown(random_choice)
#         except TelegramError:
#             update.message.reply_text(random_choice)
#
#
# def dice(bot: Bot, update: Update, args: List[str]) -> None:
#     faces = 6
#     if args:
#         try:
#             faces = int(args[0])
#             assert faces > 1
#         except ValueError:
#             update.message.reply_text("That's not a number!")
#         except AssertionError:
#             update.message.reply_text("The number must be larger than 1!")
#         else:
#             choice(bot, update, num=faces)
#
#
# def coin(bot: Bot, update: Update) -> None:
#     choice(bot, update)
#
#
# def shuffle(bot: Bot, update: Update) -> None:
#     pass
#
#
# def rand_range(bot: Bot, update: Update):
#     try:
#         sep_args = separator(update.message.text.split(max_split=2)[1])
#     except IndexError:
#         update.message.reply_markdown("Refer to [this post]() on how to use this command.")
#     else:
#
#         try:
#             pass
#         except ValueError:
#             update.message.reply_text("Given number(s) must be integers!")
#         else:
#             count = len(sep_args)
#             if count == 1:
#                 if sep_args[0] < 2:
#                     update.message.reply_text("Given number must be equal to or larger than 2!")
#                     return
#                 update.message.reply_markdown(f"`{random.randrange(sep_args[0])}`")
