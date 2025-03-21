import asyncio
import json
import re
import os
from pyrogram import filters, Client
from pyrogram.types.messages_and_media import Message

from app import app, logger
from app.models import ASession
from app.models.redpocket import Redpocket
from app.filters import custom_filters
from app.config import setting

TARGET = -1001833464786

BOT_ID = 5697370563


@app.on_message(
    filters.chat(TARGET) & filters.reply & filters.me & filters.command("fdajie")
)
async def fdajie(client: Client, message: Message):
    count = int(message.command[1])
    if len(message.command) > 2:
        new_first_name = message.command[2]
        new_last_name = message.command[3] if len(message.command) > 3 else ""
    else:
        new_first_name = message.reply_to_message.from_user.first_name
        new_last_name = message.reply_to_message.from_user.last_name
    reply_message_id = message.reply_to_message.id
    await message.delete()
    if not os.path.exists("downloads/photo.jpg"):  # 下载头像
        async for photo in client.get_chat_photos(BOT_ID, 1):
            await client.download_media(photo.file_id, file_name="photo.jpg")
    first_name = client.me.first_name
    last_name = client.me.last_name
    await client.update_profile(new_first_name, new_last_name)  # 更新名字
    await client.set_profile_photo(photo="downloads/photo.jpg")  # 更新头像
    r_message = await client.send_message(
        TARGET, f"/dajie {count}", reply_to_message_id=reply_message_id
    )

    await asyncio.sleep(1)
    await r_message.delete()
    await client.update_profile(first_name, last_name)  # 恢复名字
    async for photo in client.get_chat_photos(977495459, 1):
        await client.delete_profile_photos(photo.file_id)  # 删除头像


@app.on_message(filters.me & filters.command("gphoto") & filters.reply)
async def gphoto(client: Client, message: Message):
    async for photo in client.get_chat_photos(message.reply_to_message.from_user.id, 1):
        await client.download_media(photo.file_id, file_name="photo.jpg")
    await message.edit("已获取目标用户头像")


@app.on_message(filters.me & filters.command("sphoto"))
async def sphoto(client: Client, message: Message):
    await client.set_profile_photo(photo="downloads/photo.jpg")
    await message.delete()


@app.on_message(filters.me & filters.command("rphoto"))
async def rphoto(client: Client, message: Message):
    async for photo in client.get_chat_photos("me", 1):
        await client.delete_profile_photos(photo.file_id)
    await message.edit("已恢复头像")



redpockets = {}


async def in_redpockets_filter(_, __, m: Message):
    return bool(m.text in redpockets)
    

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
