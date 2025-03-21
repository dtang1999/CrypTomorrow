import psycopg2

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_NAME = "crypto_db"
DB_PORT = "5432"


def connect_db():
    """连接 PostgreSQL 数据库"""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    return conn
