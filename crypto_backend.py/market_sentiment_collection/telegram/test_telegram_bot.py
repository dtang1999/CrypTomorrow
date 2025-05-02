import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))


async def send_test_message():
    try:
        if TELEGRAM_BOT_TOKEN is None or TELEGRAM_USER_ID is None:
            raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_USER_ID in .env")
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_USER_ID,
            text="✅ Test message from your Telegram bot is working!",
        )
        print("✅ Test message sent successfully.")
    except Exception as e:
        print("❌ Failed to send test message:", e)


if __name__ == "__main__":
    asyncio.run(send_test_message())
