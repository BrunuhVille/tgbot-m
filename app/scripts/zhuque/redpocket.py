import asyncio
import json
import re
from pyrogram import filters, Client
from pyrogram.types.messages_and_media import Message

from app import app, logger
from app.models import ASession
from app.models.redpocket import Redpocket
from app.filters import custom_filters
from app.config import setting

TARGET = -1001833464786

redpockets = {}


async def in_redpockets_filter(_, __, m: Message):
    return bool(m.text in redpockets)

@app.on_message(filters.chat(TARGET) & filters.reply & filters.command("fdajie"))
async def fdajie(client: Client, message: Message):
    await message.delete()
    count = int(message.command[1])
    if len(message.command) > 2:
        new_first_name = message.command[2]
        new_last_name = message.command[3] if len(message.command) > 3 else ""
    else:
        new_first_name = message.reply_to_message.from_user.first_name
        new_last_name = message.reply_to_message.from_user.last_name
    first_name = client.me.first_name
    last_name = client.me.last_name
    await client.update_profile(new_first_name, new_last_name)
    r_message = await message.reply_to_message.reply(f"/dajie {count}")
    await asyncio.sleep(1)
    await r_message.delete()
    await client.update_profile(first_name, last_name)


@app.on_message(
    filters.chat(TARGET)
    & custom_filters.zhuque_bot
    & filters.regex(r"内容: (.*)\n灵石: .*\n剩余: .*\n大善人: (.*)")
)
async def get_redpocket_gen(client: Client, message: Message):
    match = message.matches[0]
    content = match.group(1)
    while True:
        button_reply = await message.click(0)
        if m := button_reply.message:
            if m in ["已领完", "不能重复领取"]:
                return
            match = re.search(r"已获得 (\d+) 灵石", m)
            if match:
                bonus = int(match.group(1))
                async with ASession() as session:
                    async with session.begin():
                        redpocket = await Redpocket.add("zhuque", bonus, session)
                        ret_str = f"""```朱雀红包 {content} 领取成功
成功领取口令红包 {bonus} 灵石
今日领取口令红包 {redpocket.today_bonus} 灵石
累计领取口令红包 {redpocket.total_bonus} 灵石```"""
                        await client.send_message(
                            setting["zhuque"]["redpocket"]["push_chat_id"], ret_str
                        )
                return
        await asyncio.sleep(1)
