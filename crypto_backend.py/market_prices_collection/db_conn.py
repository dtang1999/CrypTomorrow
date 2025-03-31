import psycopg2
import os

# from psycopg2.extras import RealDictCursor

# 从环境变量获取数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "crypto_db")
DB_PORT = os.getenv("DB_PORT", "5432")


def connect_db():
    """连接 PostgreSQL"""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    return conn
