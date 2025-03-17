import psycopg2

# 数据库连接配置
DB_NAME = "crypto_db"
DB_USER = "postgres"
DB_PASSWORD = "password"  # 替换成你的 PostgreSQL 密码
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    """连接 PostgreSQL 数据库"""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    return conn
