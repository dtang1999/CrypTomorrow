import os
import psycopg2
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from telegram import Bot
import asyncio

# Load environment variables
load_dotenv()

# Telegram bot setup
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_ID = int(os.getenv("TELEGRAM_USER_ID"))


async def trigger_alert(message):
    print("[ALERT]", message)
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_USER_ID, text=message)
    except Exception as e:
        print("❌ Failed to send Telegram alert:", e)


def format_duration(minutes: int) -> str:
    days, rem = divmod(minutes, 1440)
    hours, mins = divmod(rem, 60)
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if mins > 0:
        parts.append(f"{mins} minute{'s' if mins != 1 else ''}")
    return " ".join(parts) or "0 minutes"


async def evaluate_alerts(
    days: int = 0,
    hours: int = 0,
    minutes: int = 30,
    threshold: float = 0.7,
    sentiment: str = "negative",
):
    """
    Scan the sentiment_db table for the past time window.
    Trigger alert if the ratio of <sentiment> exceeds <threshold>.

    Args:
        days (int): Days to include in the window
        hours (int): Hours to include in the window
        minutes (int): Minutes to include in the window
        threshold (float): Ratio threshold to trigger an alert
        sentiment (str): Sentiment to check ('positive', 'negative', or 'neutral')
    """
    if sentiment not in {"positive", "negative", "neutral"}:
        raise ValueError(
            "Invalid sentiment. Must be 'positive', 'negative', or 'neutral'"
        )

    total_minutes = days * 1440 + hours * 60 + minutes
    window_str = format_duration(total_minutes)

    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE"),
    )
    cur = conn.cursor()

    since_time = datetime.now(timezone.utc) - timedelta(minutes=total_minutes)

    query = f"""
        SELECT 
            COUNT(*) FILTER (WHERE label = %s)::float / NULLIF(COUNT(*), 0) AS sentiment_ratio,
            COUNT(*) AS total
        FROM sentiment_db
        WHERE timestamp >= %s;
    """

    cur.execute(query, (sentiment, since_time))
    result = cur.fetchone()
    sentiment_ratio, total = result if result else (0, 0)

    if sentiment_ratio is None:
        sentiment_ratio = 0.0

    print(
        f"Checked last {window_str}: {total} messages, {sentiment} ratio = {sentiment_ratio:.2%}"
    )

    if total >= 10 and sentiment_ratio > threshold:
        await trigger_alert(
            f"⚠️ {sentiment.capitalize()} sentiment spike: {sentiment_ratio:.2%} in last {window_str}"
        )

    cur.close()
    conn.close()


# Example usage
if __name__ == "__main__":
    # Check the last 6 days 6 hours for positive sentiment ratio > 70%
    asyncio.run(
        evaluate_alerts(days=6, hours=6, minutes=0, threshold=0.7, sentiment="positive")
    )
