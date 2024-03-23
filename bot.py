import os
import asyncio

from pyrogram import Client, errors, types, enums, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))

app = Client("limitbreaker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(bot: Client, msg: Message):
    await msg.reply_text("Hello, I'm a bot!")

@app.on_message(filters.command("help"))
async def help(bot: Client, msg: Message):
    await msg.reply_text("Simply add the bot to the group with atleast delete and post text permissions.")

@app.on_message(filters.group & filters.text)
async def filter_messages(client, message):
    # Get the list of banned words
    banned_words_file = "banned_words.txt"

# Read the banned words from the file
    with open(banned_words_file, "r") as f:
        banned_words = f.read().splitlines()

    # Check if the message contains any banned words
    for word in banned_words:
        if word in message.text.lower():
            # Delete the message
            await client.send_message(chat_id=LOG_CHANNEL,
            text=f"User {message.from_user.mention} with id `{message.from_user.id}` sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted in the group. Below is the message which he/she sent."
            )
            await message.forward(chat_id=LOG_CHANNEL)
            await message.delete()
            warn_message = await app.send_message(message.chat.id,
            f"**WARNING:** User {message.from_user.mention} sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted.\n\n__This message will be deleted in 5s__",
            )
            await asyncio.sleep(5)
            await warn_message.delete()
            break

app.run()