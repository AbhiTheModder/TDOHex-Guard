import os
import re
import requests
import socket
import urllib3
import asyncio

from pyrogram import Client, errors, types, filters
from pyrogram.types import Message

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
LOG_CHANNEL = os.getenv("LOG_CHANNEL")

CRYPTO_WORDS = {
    "USDT",
    "gas fee",
    "bitcoin",
    "ethereum",
    "ripple",
    "litecoin",
    "blockchain",
    "cryptocurrency",
    "mining",
    "exchange",
    "ICO (Initial Coin Offering)",
    "altcoin",
    "market cap",
    "smart contract",
    "DApp (Decentralized Application)",
    "DeFi Platform",
    "decentralized",
    "Just a moment...",
}

app = Client("limitbreaker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start") & filters.private)
async def start(bot: Client, msg: Message):
    await msg.reply_text("Hello, I'm a bot! Send /help to know more.")


@app.on_message(filters.command("help") & filters.private)
async def help(bot: Client, msg: Message):
    await msg.reply_text(
        "Simply add the bot to the group with atleast delete and post text permissions."
    )


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
            if LOG_CHANNEL is not None:
                await client.send_message(
                    chat_id=int(LOG_CHANNEL),
                    text=f"User {message.from_user.mention} with id `{message.from_user.id}` sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted in the group. Below is the message which he/she sent.",
                )
                await message.forward(chat_id=LOG_CHANNEL)
            await message.delete()
            warn_message = await app.send_message(
                message.chat.id,
                f"**WARNING:** User {message.from_user.mention} sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted.\n\n__This message will be deleted in 5s__",
            )
            await asyncio.sleep(5)
            await warn_message.delete()
            break

    urls = re.findall(r"(?:https?://)?[\w/.-]+(?:\.[\w/.-]+)+", message.text)

    for url in urls:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        try:
            response = requests.get(url)
            response_text = response.text.lower()
            if any(word.lower() in response_text for word in CRYPTO_WORDS):
                if LOG_CHANNEL is not None:
                    await client.send_message(
                        chat_id=int(LOG_CHANNEL),
                        text=f"User {message.from_user.mention} with id `{message.from_user.id}` sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted in the group. Below is the message which he/she sent.",
                    )
                    await message.forward(chat_id=LOG_CHANNEL)
                await message.delete()
                warn_message = await app.send_message(
                    message.chat.id,
                    f"**WARNING:** User {message.from_user.mention} sent a message containing a banned word or a link which seems to be fraudulant and their message has been deleted.\n\n__This message will be deleted in 5s__",
                )
                await asyncio.sleep(5)
                await warn_message.delete()
                break
        except (
            requests.exceptions.ConnectionError,
            urllib3.exceptions.NameResolutionError,
            requests.exceptions.RetryError,
            socket.gaierror,
            requests.exceptions.Timeout,
        ):
            await message.delete()
            warn_message = await app.send_message(
                message.chat.id,
                f"**WARNING:** User {message.from_user.mention} sent a message containing a link **which isn't accessible(maybe dead?)** and as such their message has been deleted, If you think this is a mistake please report to Group Administrators.\n\n__This message will be deleted in 5s__",
            )
            await asyncio.sleep(5)
            await warn_message.delete()


app.run()
