import psycopg2
import os


def insert_matched_post(
    message_id,
    text,
    summary,
    keywords,
    timestamp,
    channel,
    label,
    score,
    classified=True,
):
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        dbname=os.getenv("PG_DATABASE"),
    )
    cur = conn.cursor()

    # Ensure the table exists with all necessary fields
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS sentiment_db (
            id SERIAL PRIMARY KEY,
            message_id BIGINT NOT NULL,
            text TEXT NOT NULL,
            summary TEXT,
            keywords TEXT[] NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL,
            channel TEXT NOT NULL,
            classified BOOLEAN DEFAULT FALSE,
            label VARCHAR(10),
            score FLOAT,
            UNIQUE (message_id, channel)
        );
    """
    )

    # Insert with all fields
    cur.execute(
        """
        INSERT INTO sentiment_db (
            message_id, text, summary, keywords, timestamp, channel,
            classified, label, score
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (message_id, channel) DO NOTHING;
    """,
        (
            message_id,
            text,
            summary,
            keywords,
            timestamp,
            channel,
            classified,
            label,
            score,
        ),
    )

    conn.commit()
    cur.close()
    conn.close()
