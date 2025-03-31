import psycopg2
import os
import time

def wait_for_db():
    """等待数据库就绪"""
    max_retries = 5
    retry_interval = 5
    
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "crypto_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "password"),
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432")
            )
            conn.close()
            print("✅ 数据库连接成功")
            return True
        except psycopg2.OperationalError:
            if i < max_retries - 1:
                print(f"等待数据库就绪... ({i+1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                print("❌ 无法连接到数据库")
                return False

def init_db():
    """初始化数据库表"""
    if not wait_for_db():
        return False

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "crypto_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "password"),
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432")
    )
    cursor = conn.cursor()

    try:
        # 创建表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto_prices (
            timestamp TIMESTAMPTZ,
            symbol TEXT NOT NULL,
            open NUMERIC,
            high NUMERIC,
            low NUMERIC,
            close NUMERIC,
            volume NUMERIC,
            PRIMARY KEY (timestamp, symbol)
        );
        """)

        # 创建索引
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_crypto_prices_timestamp 
        ON crypto_prices(timestamp);
        """)

        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_crypto_prices_symbol 
        ON crypto_prices(symbol);
        """)

        conn.commit()
        print("✅ 数据库表创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建数据库表失败: {str(e)}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db() 