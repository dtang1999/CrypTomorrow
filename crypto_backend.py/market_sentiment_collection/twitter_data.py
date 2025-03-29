import os
import tweepy
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API 密钥
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# 创建客户端
client = tweepy.Client(bearer_token=BEARER_TOKEN)


def get_tweets(keyword="Bitcoin", max_results=100):
    """从 Twitter 获取推文数据"""
    tweets = client.search_recent_tweets(
        query=keyword,
        max_results=max_results,
        tweet_fields=["created_at", "text", "author_id", "public_metrics", "lang"],
    )

    tweet_data = []
    if tweets.data:
        for tweet in tweets.data:
            if tweet.lang == "en":
                tweet_data.append(
                    [
                        tweet.created_at,
                        tweet.text,
                        tweet.author_id,
                        tweet.public_metrics["retweet_count"],
                        tweet.public_metrics["like_count"],
                    ]
                )

    return tweet_data


if __name__ == "__main__":
    tweets = get_tweets("Bitcoin")
    print(tweets[:5])
