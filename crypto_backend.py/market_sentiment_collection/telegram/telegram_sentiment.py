import asyncio

# from telegram_data import fetch_telegram_texts, parse_datetime_custom
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Initialize FinBERT model
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
finbert_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


def get_sentiment(text):
    """
    Returns a dictionary with sentiment label and confidence score.
    """
    if not text.strip():
        return {"label": "neutral", "score": 0.0}
    result = finbert_pipeline(text[:512])[0]
    return {"label": result["label"], "score": round(result["score"], 4)}


# async def run_analysis():
#     """
#     Fetch matched Telegram posts and analyze their sentiment using FinBERT.
#     """
#     channel = "binancekillers"
#     start_time = parse_datetime_custom("04/25/2025 00:00")
#     texts = await fetch_telegram_texts(
#         channel_username=channel, limit=30, start_time=start_time
#     )

#     print(f"Fetched {len(texts)} matched messages\n")

#     for item in texts:
#         sentiment = get_sentiment(item["text"])
#         print("Text preview:", item["text"][:200])
#         print("Sentiment:", sentiment["label"], f"(score={sentiment['score']})")
#         print("Keywords:", item["keywords"])
#         print("Timestamp:", item["timestamp"])
#         print("=" * 40)


if __name__ == "__main__":
    # asyncio.run(run_analysis())
    pass
