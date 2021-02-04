import os
from .terminal import Terminal

from pyrogram import Client, filters
from pyrogram.types import Message

terminal = Terminal()
OWNER_ID = int(os.environ.get("OWNER_ID, 0))

bot = Client(
    session_name=":memory:",
    api_id=int(os.environ.get("API_ID", 0)),
    api_hash=os.environ.get("API_HASH", None),
    bot_token=os.environ.get("BOT_TOKEN", None)
)


@bot.on_message(filters.command("start"))
async def _start(_, msg: Message):
    START = """
Hi I am Terminal Bot which will Execute your Commands.
if you wanna build your own bot, deploy from [here](https://github.com/Krishna-Singhal/Terminal-Bot).
"""
    await msg.reply(START.format(msg.from_user.mention))


@bot.on_message(filters.command("term) & filters.user(OWNER_ID))
async def exec_cmd(_, msg: Message):
    if not len(msg.command) > 1:
        return await msg.reply("`Command not found!`")
    response = terminal.ex_command(msg.command[1]);
    while len(response) > 0:
        await bot.send_message(msg.chat_id, text=response[0:4000]);
        response=response[4000:]


if __name__ == "__main__":
    bot.run()
