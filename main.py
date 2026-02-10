import asyncio
from pyrogram import idle
from app import app, models, scripts

async def main():
    await app.start()
    await models.create_all()
    await idle()
    await app.stop()

if __name__ == "__main__":
    # 【新代码】使用 get_event_loop 避免不同 loop 冲突
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    # 【旧代码备份】原 app.run 写法在当前 pyrogram 版本不兼容
    """
    app.run(main())
    """
