import os
import asyncio
from getpass import getuser
from os import geteuid
from terminal import Terminal

from pyrogram import Client, filters
from pyrogram.types import Message

OWNER_ID = int(os.environ.get("OWNER_ID", 0))

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


@bot.on_message(filters.command("term") & filters.user(OWNER_ID))
async def exec_cmd(_, msg: Message):
    if not len(msg.command) > 1:
        return await msg.reply("`Command not found!`")
    cmd = msg.command[1]
    try:
        t_obj = await Terminal.execute(cmd)
    except Exception as t_e:
        await msg.reply(f"**ERROR:** `{t_e}`")
        return
    curruser = getuser()
    try:
        uid = geteuid()
    except ImportError:
        uid = 1
    output = f"`{curruser}:~#` `{cmd}`\n" if uid == 0 else f"`{curruser}:~$` `{cmd}`\n"
    count = 0
    k = None
    while not t_obj.finished:
        count += 1
        await asyncio.sleep(0.5)
        if count >= 5:
            count = 0
            out_data = f"{output}`{t_obj.read_line}`"
            k = await msg.reply(out_data)
    out_data = f"`{output}{t_obj.get_output}`"
    if len(out_data) > 4096:
        if k:
            await k.delete()
        with open("terminal.txt", "w+") as ef:
            ef.write(out_data)
            ef.close()
        await msg.reply_document(
            "terminal.txt", filename="terminal.txt", caption=cmd)
        os.remove("terminal.txt")
        return
    send = msg.edit if k else msg.reply
    await send(out_data)


if __name__ == "__main__":
    bot.run()
