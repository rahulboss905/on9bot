import logging
import sys
import os
import asyncio
from threading import Thread
from typing import List

# Updated imports for v20.x
from telegram import (
    Update, ChatMember, ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardMarkup, InlineKeyboardButton, Chat, Bot, Message, User
)
from telegram.constants import ChatAction, ParseMode
from telegram.error import TimedOut, TelegramError
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes,
    filters, ApplicationBuilder
)
from telegram.helpers import escape_markdown

import config
from utils import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Check if given information is valid
assert config.BOT_TOKEN != "", "Provide a bot token!"
assert config.OWNER_ID > 0, "Provide a valid user id!"
assert config.OWNER_USERNAME, "Set a username! Go to Settings > Username to do so."
assert config.ADMIN_GROUP_ID < 0, "Set a group, supergroup or channel as the admin group!"
for uid in config.CAN_USE_TAG9:
    assert uid > 0, "You can only append CAN_USE_TAG9 with valid user ids!"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(
        f"Use /help to see my functions. Contact {config.OWNER_MENTION} if you have questions, "
        "suggestions or found a typo or error."
    )


async def bot_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(f"[Help and Source Code]({config.GITHUB_SOURCE_CODE_LINK})")


async def tag9js(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat = msg.chat
    if chat.id == config.SPECIAL_GROUP_ID or (msg.from_user.id == config.OWNER_ID and chat.type in (Chat.GROUP, Chat.SUPERGROUP)):
        await chat.send_action(ChatAction.TYPING)
        try:
            js_info = await chat.get_member(190726372)
            assert js_info.status in (ChatMember.CREATOR, ChatMember.ADMINISTRATOR, ChatMember.MEMBER)
        except (TelegramError, AssertionError):
            await msg.reply_text("no u, he is not in this group")
            return
        if js_info.user.username:
            username = "@" + js_info.user.username
            try:
                text = msg.text.split(maxsplit=1)[1]
                if "@" in text or text.startswith(("/", ".", "#", "!", "?")):
                    raise IndexError
                assert "{username}" in text
                text = text.replace("{username}", username)
            except IndexError:
                text = username
            except AssertionError:
                text = f"{msg.text.split(maxsplit=1)[1]} {username}"
            sent = await msg.reply_text(
                "15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
                reply_markup=ReplyKeyboardMarkup([[text]]),
                quote=True
            )
            await asyncio.sleep(15)
            await del_msg(sent)
            await msg.reply_text(
                "Tag9js over, removed reply keyboard and deleted message if no one did so...",
                reply_markup=ReplyKeyboardRemove(),
                quote=False
            )
        else:
            await msg.reply_text("no u, JS removed username.")
    elif chat.id < 0:
        await msg.reply_text("no u")
    else:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(
            "Join HK Duker", url="https://t.me/hkduker")]])
        await msg.reply_text("This command can only be used in HK Duker.", reply_markup=reply_markup)


async def tag9(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    chat = msg.chat
    args = context.args
    await chat.send_action(ChatAction.TYPING)
    if msg.from_user.id not in config.CAN_USE_TAG9 or msg.chat_id > 0:
        await msg.reply_text("no u")
    elif msg.reply_to_message:
        u_info = await chat.get_member(msg.reply_to_message.from_user.id)
        await tag9_part2(msg, u_info)
    elif not args:
        await msg.reply_text("Please reply to a user's message or provide a valid user id as an argument.")
    else:
        try:
            nub_id = int(args[0])
            assert nub_id > 0
            u_info = await chat.get_member(nub_id)
            await tag9_part2(msg, u_info)
        except (ValueError, AssertionError):
            await msg.reply_text("no u, user ids only.")
        except TimedOut:
            pass
        except TelegramError:
            await msg.reply_text("no u, give a valid user id.")


async def tag9_part2(msg: Message, u_info: ChatMember) -> None:
    if u_info.status in (ChatMember.LEFT, ChatMember.RESTRICTED, ChatMember.KICKED):
        await msg.reply_text("no u, not in group or restricted")
    elif u_info.user.id in (config.OWNER_ID, context.bot.id):
        await msg.reply_text("no u")
    elif u_info.user.is_bot:
        await msg.reply_text("no u, don't tag other bots.")
    elif not u_info.user.username:
        await msg.reply_text("no u, user has no username.")
    else:
        sent = await msg.reply_text(
            "15 sec, tag tag tag. Use /remove_keyboard to remove the reply keyboard.",
            reply_markup=ReplyKeyboardMarkup([[u_info.user.name]])
        )
        await asyncio.sleep(15)
        await del_msg(sent)
        await msg.reply_text(
            "Tag9 over, removed reply keyboard and deleted message if no one did so...",
            reply_markup=ReplyKeyboardRemove(),
            quote=False
        )


async def remove_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if msg.chat_id > 0:
        await msg.reply_text("no u")
        return
    sent = await msg.reply_text(
        "Replacing reply keyboard markup if there was an existing one...",
        reply_markup=ReplyKeyboardMarkup([["I AM A STUPID ANIMAL THAT LIKES TO CLICK REPLY KEYBOARD BUTTONS"]]),
        quote=False
    )
    await del_msg(sent)
    await msg.reply_text(
        "Removed reply keyboard...",
        reply_markup=ReplyKeyboardRemove(),
        quote=False
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    rmsg = msg.reply_to_message
    try:
        text = msg.text.split(maxsplit=1)[1]
        try:
            if msg.from_user.id != config.OWNER_ID:
                echo_owner_check(text)
            if rmsg:  # if message has args and replies to another message
                await rmsg.reply_markdown(text, disable_web_page_preview=True)
            else:  # if message has args and does not reply to another message
                await msg.reply_markdown(text, disable_web_page_preview=True, quote=False)
        except AssertionError:
            await msg.reply_text("Tag your mother?!")
        except TimedOut:
            pass
        except TelegramError as e:
            await msg.reply_text(config.MARKDOWN_ERROR_TEXT.format(str(e)))
        else:
            await del_msg(msg)
    except IndexError:
        if not rmsg:  # if message has no arguments and does not reply to another message
            await msg.reply_markdown("no u, use `/r [text]` or reply to a message (or both).")
        elif not rmsg.text:  # if message has no arguments and replied message does not have text
            await msg.reply_text("no u, messages with text only.")
        else:  # if message has no arguments and replies to a message with text
            text = rmsg.text_markdown
            try:
                if msg.from_user.id != config.OWNER_ID:
                    echo_owner_check(text)
                await msg.reply_markdown(text, disable_web_page_preview=True, quote=False)
            except AssertionError:
                await msg.reply_text("Tag your mother?!")
            except TimedOut:
                pass
            except TelegramError as e:
                await msg.reply_text(config.MARKDOWN_ERROR_TEXT.format(str(e)))
            else:
                await del_msg(msg)


async def stalk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    chat = msg.chat
    await chat.send_action(ChatAction.TYPING)
    user = rmsg.forward_from if rmsg and rmsg.forward_from else rmsg.from_user if rmsg else msg.from_user
    title = f"[{chat.title}](t.me/{chat.username})" if chat.username else f"[{chat.title}]({chat.invite_link})" \
        if chat.invite_link else f"*{chat.title}*"
    text = f"*{'Bot' if user.is_bot else 'User'} info*"
    text += f"\n\nName: {user.mention_markdown(user.full_name)}\nUser id: `{user.id}`"
    if user.username:
        text += f"\nUsername: @{escape_markdown(user.username)}"
    if user.language_code:
        text += f"\nLanguage code: {user.language_code}"
    try:
        assert chat.type in (Chat.GROUP, Chat.SUPERGROUP)
        nub = await chat.get_member(user.id)
        s = nub.status
    except (TelegramError, AssertionError):
        await msg.reply_markdown(text, disable_web_page_preview=True)
        return
    if s == ChatMember.CREATOR:
        text += f"\n\n*Creator* of {title}"
    elif s == ChatMember.ADMINISTRATOR:
        text += f"\n\n*Administrator* of {title}"
        text += f"\nCan change group info: {yn_processor(nub.can_change_info)}"
        text += f"\nCan delete messages: {yn_processor(nub.can_delete_messages)}"
        text += f"\nCan restrict, ban and unban members: {yn_processor(nub.can_restrict_members)}"
        text += f"\nCan pin messages: {yn_processor(nub.can_pin_messages)}"
        text += f"\nCan promote members to admins: {yn_processor(nub.can_promote_members)}"
    elif s == ChatMember.MEMBER:
        text += f"\n\n*Member* of {title}"
    elif s == ChatMember.RESTRICTED:
        text += f"\n\n*Restricted* in {title}"
        text += f"\n\nCan send messages: {yn_processor(nub.can_send_messages)}"
        if nub.can_send_messages:
            text += f"\nCan send media: {yn_processor(nub.can_send_media_messages)}"
            if nub.can_send_media_messages:
                text += f"\nCan send stickers and GIFs: {yn_processor(nub.can_send_other_messages)}"
                text += f"\nCan add web page previews: {yn_processor(nub.can_add_web_page_previews)}"
    elif s == ChatMember.LEFT:
        text += f"\n\n*Not a member* of {title}"
    elif s == ChatMember.KICKED:
        text += f"\n\n*Banned* from {title}"
    await msg.reply_markdown(text, disable_web_page_preview=True)


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    if rmsg:
        ff = rmsg.forward_from
        await msg.reply_markdown(f"`{ff.id if ff else rmsg.from_user.id}`")
    else:
        user_id = msg.from_user.id
        if msg.chat_id > 0:
            await msg.reply_markdown(f"`{user_id}`")
        else:
            await msg.reply_markdown(f"Chat id: `{msg.chat_id}`\nYour user id: `{user_id}`")


async def get_message_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        await msg.reply_text("no u, reply to a message")
        return
    chat = msg.chat
    if chat.type == Chat.SUPERGROUP and chat.username:
        await msg.reply_markdown(f"```https://t.me/{chat.username}/{rmsg.id}```")
    else:
        await msg.reply_markdown(f"no u, can only be used in public supergroup, but the replied message's id is `{rmsg.id}`.")


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    if not rmsg:
        await msg.reply_text("no u, reply to a message")
        return
    if rmsg.audio:
        await gfi_response(msg, "audio", rmsg.audio.file_id)
    elif rmsg.photo:
        await gfi_response(msg, "picture", rmsg.photo[-1].file_id)
    elif rmsg.sticker:
        await gfi_response(msg, "sticker", rmsg.sticker.file_id)
    elif rmsg.video:
        await gfi_response(msg, "video", rmsg.video.file_id)
    elif rmsg.voice:
        await gfi_response(msg, "voice recording", rmsg.voice.file_id)
    elif rmsg.video_note:
        await gfi_response(msg, "video", rmsg.video_note.file_id)
    elif rmsg.document:
        await gfi_response(msg, "document", rmsg.document.file_id)
    else:
        await msg.reply_text("no u, message has no media.")


async def gfi_response(msg: Message, file_type: str, file_id: str) -> None:
    await msg.reply_markdown(f"File id of this {file_type}: `{file_id}`")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown("Ping your mother?!")


async def pinned(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    chat = msg.chat
    if chat.type != Chat.SUPERGROUP:
        await msg.reply_text("no u, supergroups only")
        return
    chat_info = await context.bot.get_chat(chat.id)
    pmsg = chat_info.pinned_message
    if not pmsg:
        await msg.reply_text("No pinned message (sometimes wrong, unstable function)")
        return
    p_id = pmsg.message_id
    if not pmsg.from_user.is_bot or pmsg.from_user.id == context.bot.id:
        await pmsg.reply_text("⬆️Pinned message⬆️")
    elif chat.username:
        link = f"https://t.me/{chat.username}/{p_id}"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Pinned message", url=link)]])
        await msg.reply_text("⬇️Pinned message⬇️", reply_markup=reply_markup)
    else:
        await msg.reply_text(f"no u, sender is bot and group is private, but the pinned message's id is `{p_id}`.")


async def slap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    if rmsg:
        await rmsg.reply_text("Oof!")
    else:
        await msg.reply_text("Oof!")


async def owner_edit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    rmsg = msg.reply_to_message
    if msg.from_user.id != config.OWNER_ID:
        await msg.reply_text("no u")
    elif not rmsg:
        await msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != context.bot.id:
        await msg.reply_text("no u, not my message")
    else:
        try:
            await rmsg.edit_text(
                msg.text.split(maxsplit=1)[1],
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            await del_msg(msg)
        except IndexError:
            await msg.reply_text("no u, no args")
        except TimedOut:
            pass
        except TelegramError as e:
            await msg.reply_markdown(escape_markdown(str(e)))


async def owner_delmsg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    rmsg = msg.reply_to_message
    if msg.from_user.id != config.OWNER_ID:
        await msg.reply_text("no u")
    elif not rmsg:
        await msg.reply_text("no u, reply to a message")
    elif rmsg.from_user.id != context.bot.id:
        await msg.reply_text("no u, not my message")
    else:
        await del_msg(rmsg)
        await del_msg(msg)


async def service_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if msg.new_chat_members:
        for nub in msg.new_chat_members:
            if nub.id == context.bot.id:
                await msg.reply_markdown(
                    f"Use /help to see my functions. Contact {config.OWNER_MENTION} if you have questions, "
                    "suggestions or found typos or errors.",
                    quote=False
                )
            elif nub.is_bot:
                await msg.reply_text("Ooh, new bot!")
            elif msg.chat.id == config.SPECIAL_GROUP_ID and check_number_man(nub):
                await kick_member(msg.chat, nub.id)
    elif msg.left_chat_member:
        await msg.reply_text("Bey.")


async def number_man_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    await kick_member(msg.chat, msg.from_user)


async def owner_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.effective_message.reply_markdown(
        f"Hi {config.OWNER_MENTION}! "
        "Would you like JS with Spaghetti or Double Decker JS Hamburger for lunch?",
        disable_web_page_preview=True
    )


async def no_u_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    no_count = max([p.count("no") for p in
                    [s.strip() for s in msg.text.lower().split("u") if "no" in s]])
    if no_count < 100:
        await msg.reply_text(f"{'no ' * (no_count + 1)}u")
    else:
        await msg.reply_sticker("CAADBAADSgIAAvkw6QXmVrbEBht6SAI")


async def other_msg_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user = msg.from_user
    text = msg.text.lower()
    if user.id != config.OWNER_ID and msg.chat_id < 0 and config.OWNER_USERNAME.lower() in text:
        await msg.reply_text("Tag your mother?!")
    elif text == "js is very on9":
        await msg.reply_text("Your IQ is 500!")
    elif text == "trainer jono is rubbish":
        await msg.reply_voice("AwADBQADTAADJOWZVNlBR4Cek06kAg")
    elif "but can you do this" in text:
        await msg.reply_sticker("CAADBAADbwIAAvkw6QUeD3c89PLAOAI")
    elif text == "goodest english":
        await msg.reply_voice("AwADBQADJgAD8KLQVNdHdLAHdLMzAg")
    elif text == "my english is very good":
        await msg.reply_voice("AwADBQADJwAD8KLQVFu-e5gh4i8RAg")
    elif "too good" in text or "very good" in text:
        await msg.reply_voice("AwADBQADKAAD8KLQVHrlKTFsd-qGAg")


async def ketchup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    await context.bot.forward_message(-1001312239961, -1001208896598, msg.message_id)


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    user = msg.from_user
    chat = msg.chat
    try:
        chat_link = f"https://t.me/{chat.username}" if chat.username and chat.id < 0 else None
        chat_name = f"[{chat.title}]({chat_link}) (chat id: `{chat.id}`)" if chat.id < 0 else "pm"
        fb = escape_markdown(msg.text.split(maxsplit=1)[1])
        fb = (f"Feedback for {config.BOT_USERNAME} from {user.mention_markdown(user.full_name)} (user id: `{user.id}`) "
              f"sent in {chat_name}:\n\n{fb}")
        if chat_link:
            message_link = f"{chat_link}/{msg.message_id}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Message", url=message_link)]])
            await context.bot.send_message(
                config.ADMIN_GROUP_ID,
                fb,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
        else:
            await context.bot.send_message(
                config.ADMIN_GROUP_ID,
                fb,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        await msg.reply_text("Feedback sent successfully!")
    except IndexError:
        await msg.reply_text("no u, put some constructive text behind it")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    try:
        if "Timed out" in str(context.error):
            return
            
        if update is None or not hasattr(update, 'message'):
            return
            
        msg = update.message
        chat = msg.chat
        error = escape_markdown(str(context.error))
        forwarded = await msg.forward(config.ADMIN_GROUP_ID)
        chat_link = f"https://t.me/{chat.username}" if chat.username and chat.id < 0 else None
        chat_name = f"[{chat.title}]({chat_link}) (chat id: `{chat.id}`)" if chat.id < 0 else "pm"
        text = f"Error occurred in {chat_name}:\n\n{error}"
        
        if chat_link:
            message_link = f"{chat_link}/{msg.message_id}"
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Message", url=message_link)]])
            await forwarded.reply_markdown(text, reply_markup=reply_markup, disable_web_page_preview=True)
        else:
            await forwarded.reply_markdown(text, disable_web_page_preview=True)
        
        await msg.reply_text(
            f"This message caused an error: {error}\nThe message was forwarded to the creator and he will "
            "try to fix it."
        )
    except TelegramError:
        pass


async def main() -> None:
    # Initialize application
    application = ApplicationBuilder().token(config.BOT_TOKEN).build()
    
    # Fetch bot information asynchronously
    bot_info = await application.bot.get_me()
    config.BOT_USERNAME = bot_info.username
    logger.info(f"Bot initialized with username: @{config.BOT_USERNAME}")
    
    # Define restart function
    def stop_and_restart():
        application.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        msg = update.message
        if msg.from_user.id != config.OWNER_ID:
            await msg.reply_text("no u")
        else:
            await msg.reply_text("Restarting bot...")
            Thread(target=stop_and_restart).start()
    
    # Commands for all users
    application.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    application.add_handler(CommandHandler("help", bot_help))
    application.add_handler(CommandHandler("tag9", tag9))
    application.add_handler(CommandHandler("tag9js", tag9js))
    application.add_handler(CommandHandler("remove_keyboard", remove_keyboard))
    application.add_handler(CommandHandler("r", echo))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("link", get_message_link))
    application.add_handler(CommandHandler("pinned", pinned))
    application.add_handler(CommandHandler("file_id", get_file_id))
    application.add_handler(CommandHandler("stalk", stalk))
    application.add_handler(CommandHandler("feedback", feedback))
    
    # Commands for the owner
    application.add_handler(CommandHandler(["exec", "ex"], owner_exec))
    application.add_handler(CommandHandler("edit", owner_edit))
    application.add_handler(CommandHandler("delmsg", owner_delmsg))
    application.add_handler(CommandHandler("restart", restart))
    
    # Message handlers
    application.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS | filters.StatusUpdate.LEFT_CHAT_MEMBER,
        service_msg_handler
    ))
    application.add_handler(MessageHandler(
        filters.Chat(config.SPECIAL_GROUP_ID) & check_number_man_filter & bot_is_admin_filter,
        number_man_handler
    ))
    application.add_handler(MessageHandler(
        filters.User(config.OWNER_ID) & filters.TEXT & filters.Regex(r"(?i)hello"),
        owner_msg_handler
    ))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.Regex(r"(?i).*(no)+ u"),
        no_u_handler
    ))
    application.add_handler(MessageHandler(
        filters.Chat(config.SPECIAL_GROUP_ID) & filters.TEXT,
        other_msg_handler
    ))
    application.add_handler(MessageHandler(
        filters.Chat(-1001208896598),
        ketchup
    ))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    debug = os.environ.get("DEBUG")
    if debug != "yes":
        await application.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 80)),
            url_path=config.BOT_TOKEN,
            webhook_url=f"https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.BOT_TOKEN}"
        )
    else:
        await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())