import asyncio
import json
from telegram_data import fetch_and_store_channel_data, parse_datetime_custom
import os

# File paths for channel and keyword mapping
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_CHANNEL_LIST = os.path.join(BASE_DIR, "config", "channels.txt")
CONFIG_KEYWORD_MAP = os.path.join(BASE_DIR, "config", "keyword_map.json")


def load_channel_config():
    """
    Loads the list of Telegram channels and their corresponding keyword file mapping.

    Returns:
        channels (List[str]): List of channel usernames.
        keyword_map (Dict[str, str]): Mapping of channel name to keyword filename.
    """
    with open(CONFIG_CHANNEL_LIST, "r") as f:
        channels = [line.strip() for line in f if line.strip()]

    with open(CONFIG_KEYWORD_MAP, "r") as f:
        keyword_map = json.load(f)

    return channels, keyword_map


async def run_batch(limit: int, start_time_str: str):
    """
    Batch process multiple Telegram channels:
    - Fetch messages
    - Match keywords
    - Generate summary
    - Run sentiment classification
    - Insert to database

    Args:
        limit (int): Max number of messages to fetch per channel.
        start_time_str (str): Starting point in "MM/DD/YYYY HH:MM" format (UTC).
    """
    channels, keyword_map = load_channel_config()
    start_time = parse_datetime_custom(start_time_str)

    for channel in channels:
        # keyword_file = keyword_map.get(channel, "default.txt")
        keyword_file = "default.txt"
        keyword_path = f"{keyword_file}"
        print(f"\n🚀 Processing channel: {channel} (Keywords: {keyword_path})")
        await fetch_and_store_channel_data(
            channel_username=channel,
            limit=limit,
            start_time=start_time,
            keyword_file=keyword_path,
        )


if __name__ == "__main__":
    limit = 20
    start_time_str = "04/25/2025 00:00"
    asyncio.run(run_batch(limit=limit, start_time_str=start_time_str))
