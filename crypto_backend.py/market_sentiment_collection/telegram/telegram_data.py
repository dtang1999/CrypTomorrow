import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
from datetime import datetime, timezone

from db_utils import insert_matched_post
from text_utils import summarize_text
from telegram_sentiment import get_sentiment

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone_number = os.getenv("PHONE")


def load_keywords_from_file(file_name):
    base_path = os.path.dirname(__file__)
    keywords_dir = os.path.join(base_path, "keywords")
    file_path = os.path.join(keywords_dir, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"关键词文件找不到：{file_path}")
    keywords = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            kw = line.strip()
            if kw:
                keywords.append(kw.lower())
    return keywords


def extract_matched_keywords(text, keywords):
    if not text:
        return []
    text = text.lower()
    return [kw for kw in keywords if kw in text]


def extract_matched_keywords_autosplit(text, keywords):
    """
    Matches keywords or their sub-words in the input text.

    Multi-word keywords are split, and any matching part counts.
    Returns a list of matched sub-keywords (lowercase, unique).
    """
    if not text:
        return []
    text = text.lower()
    matched = set()
    for kw in keywords:
        if " " in kw:
            for sub_kw in kw.split():
                if sub_kw in text:
                    matched.add(sub_kw)
        elif kw in text:
            matched.add(kw)
    return list(matched)


def parse_datetime_custom(date_str):
    dt = datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    return dt.replace(tzinfo=timezone.utc)


async def fetch_and_store_channel_data(
    channel_username, limit, start_time, keyword_file
):
    session_name = f"session_{channel_username}"
    client = TelegramClient(session_name, api_id, api_hash)

    await client.start(phone=phone_number)

    print(f"📡 正在抓取频道: {channel_username} | 关键词文件: {keyword_file}")

    messages = await client.get_messages(
        channel_username,
        limit=limit,
        offset_date=start_time,
        reverse=True,
    )

    KEYWORDS = load_keywords_from_file(keyword_file)
    matched_messages = 0

    for message in messages:
        if not message.text:
            continue

        # Change below function to extract_matched_keywords_autosplit
        # to match keywords with space in the same line
        matched_keywords = extract_matched_keywords(message.text, KEYWORDS)
        if not matched_keywords:
            continue

        summary = summarize_text(message.text)
        sentiment = get_sentiment(summary)

        insert_matched_post(
            message_id=message.id,
            text=message.text,
            summary=summary,
            keywords=matched_keywords,
            timestamp=message.date,
            channel=channel_username,
            label=sentiment["label"],
            score=sentiment["score"],
            classified=True,
        )

        matched_messages += 1

    print(f"✅ 处理完成频道: {channel_username} | 命中关键词消息数: {matched_messages}")
