import psycopg2

# 数据库配置
DB_NAME = "crypto_db"
DB_USER = "postgres"
DB_PASSWORD = "password"  # 替换成你的密码
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    """连接 TimescaleDB"""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    return conn

def create_table():
    """创建 TimescaleDB 表"""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto_prices (
        timestamp TIMESTAMPTZ PRIMARY KEY,
        symbol TEXT NOT NULL,
        open NUMERIC,
        high NUMERIC,
        low NUMERIC,
        close NUMERIC,
        volume NUMERIC
    );
    """)

    # 转换为时序表
    cursor.execute("SELECT create_hypertable('crypto_prices', 'timestamp', if_not_exists => TRUE);")

    conn.commit()
    cursor.close()
    conn.close()

# 运行创建表
create_table()
