import random
from pyrogram import Client, filters
from pyrogram.types import Message
from TEAMZYRO import user_collection, app, GLOG


async def send_log_message(chat_id: int, message: str):
    """Send a log message to the specified chat."""
    await app.send_message(chat_id=chat_id, text=message)

import asyncio

@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    bot_user = await client.get_me()

    if bot_user.id in [user.id for user in message.new_chat_members]:
        added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id
        chat_username = f"@{message.chat.username}" if message.chat.username else "ᴩʀɪᴠᴀᴛ"

        # Log to admin channel
        log_message = (
            f"#newgroup\n\n"
            f"👥 Chat Name: {chat_title}\n"
            f"🔗 Username: {chat_username}\n"
            f"➕ Added By: {added_by}"
        )
        await send_log_message(LOGGER_ID, log_message)

        # Check member count
        chat_members_count = await client.get_chat_members_count(chat_id)
        if chat_members_count < 15:
            group_notice = (
                "**🚫 Sorry!**\n"
                "**This group has less than 15 members.**\n"
                
            )
            await message.reply(group_notice)  # 🟢 Message for group

            await asyncio.sleep(2)  # Wait before leaving

            # Leave the group
            await client.leave_chat(chat_id)

            # Log to admin
            leave_log = (
                f"#leftgroup\n\n"
                f"👥 Chat Name: {chat_title}\n"
                f"🔗 Username: {chat_username}\n"
                f"❌ Reason: Group has less than 15 members"
            )
            await send_log_message(LOGGER_ID, leave_log)

@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    """Handle the bot leaving the chat."""
    bot_user = await app.get_me()
    
    # Check if the bot is the one that left
    if bot_user.id == message.left_chat_member.id:
        removed_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        chat_title = message.chat.title
        chat_id = message.chat.id
        chat_username = f"@{message.chat.username}" if message.chat.username else "ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"

        # Construct the log message
        log_message = (
            f"#leftgroup \n\n"
            f"chat name : {chat_title}\n"
            f"chat username : {chat_username}\n"
            f"remove by : {removed_by}\n"
        )
        
        await send_log_message(GLOG, log_message)
