import os
import psycopg2
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# 加载 .env 环境变量
load_dotenv()

# 初始化 FinBERT 模型
MODEL_NAME = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


# 使用摘要进行情绪分类
def get_sentiment(summary_text):
    if not summary_text or not summary_text.strip():
        return {"label": "neutral", "score": 0.0}
    result = sentiment_pipeline(summary_text[:512])[0]
    return {"label": result["label"], "score": round(result["score"], 4)}


# 主逻辑：更新未分类的摘要记录
def update_unclassified_messages():
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE"),
    )
    cur = conn.cursor()

    # 从数据库获取未分类且摘要不为空的记录
    cur.execute(
        """
        SELECT id, summary FROM sentiment_db
        WHERE classified = FALSE
        AND summary IS NOT NULL
        LIMIT 50;
        """
    )

    rows = cur.fetchall()
    print(f"Found {len(rows)} unclassified messages with summary.")

    for row in rows:
        row_id, summary_text = row
        sentiment = get_sentiment(summary_text)
        print(
            f"Updating row {row_id} → {sentiment['label']} (score={sentiment['score']})"
        )

        cur.execute(
            """
            UPDATE sentiment_db
            SET label = %s,
                score = %s,
                classified = TRUE
            WHERE id = %s;
            """,
            (sentiment["label"], sentiment["score"], row_id),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Finished updating sentiment classifications.")


# 入口
if __name__ == "__main__":
    update_unclassified_messages()
