import os
import sys
import asyncio
import logging
from getpass import getuser
from os import geteuid
from terminal import Terminal

from pyrogram import Client, filters
from pyrogram.types import Message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOG = logging.getLogger(__name__)

LOG.info("Checking Configs...")

bot = Client(
    session_name=":memory:",
    api_id=int(os.environ.get("API_ID", 0)),
    api_hash=os.environ.get("API_HASH", None),
    bot_token=os.environ.get("BOT_TOKEN", None)
)

OWNER_ID = [int(x.strip()) for x in os.environ.get("OWNER _ID", 0).split() if x.strip()]
if not OWNER_ID:
    LOG.error("Owner Id required, Exiting...")
    sys.exit()

@bot.on_message(filters.command("start"))
async def _start(_, msg: Message):
    START = """
Hi I am Terminal Bot which will Execute your Commands.
if you wanna build your own bot, deploy from [here](https://github.com/Krishna-Singhal/Terminal-Bot).
"""
    await msg.reply(START.format(msg.from_user.mention))


@bot.on_message(filters.user(OWNER_ID) & filters.text)
async def exec_cmd(_, msg: Message):
    cmd = msg.text
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
            try:
                if not k:
                    k = await msg.reply(out_data)
                else:
                    await k.edit(out_data)
            except:
                pass
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
    send = k.edit if k else msg.reply
    await send(out_data)


if __name__ == "__main__":
    bot.run()

LOG.info("Terminal-Bot initialized.")
