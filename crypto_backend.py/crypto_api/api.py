from fastapi import APIRouter, Query
import psycopg2
import redis
import json
from db import connect_db
from datetime import datetime
from decimal import Decimal

router = APIRouter()

# 连接 Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def serialize_data(data):
    """转换 datetime 和 Decimal 为可序列化格式"""
    for row in data:
        for key, value in row.items():
            if isinstance(value, datetime):
                row[key] = value.isoformat()  # datetime 转换为 ISO 格式字符串
            elif isinstance(value, Decimal):
                row[key] = float(value)  # Decimal 转换为 float
    return data

@router.get("/prices/{symbol}")
def get_prices(
    symbol: str,
    limit: int = Query(100, gt=0, lt=1000),
    offset: int = Query(0, ge=0),
    start_time: str = None,
    end_time: str = None
):
    """查询加密货币价格数据，支持分页 + Redis 缓存"""

    # 构造 Redis 缓存键
    cache_key = f"prices:{symbol}:{limit}:{offset}:{start_time or 'None'}:{end_time or 'None'}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        return json.loads(cached_data)  # 直接返回缓存数据

    # 连接数据库
    conn = connect_db()
    cursor = conn.cursor()

    # 构造 SQL 查询
    query = """
    SELECT timestamp, open, high, low, close, volume FROM crypto_prices
    WHERE symbol = %s
    """
    params = [symbol]

    if start_time and end_time:
        query += " AND timestamp BETWEEN %s AND %s"
        params.append(start_time)
        params.append(end_time)

    query += " ORDER BY timestamp DESC LIMIT %s OFFSET %s"
    params.append(limit)
    params.append(offset)

    # 查询数据库
    cursor.execute(query, tuple(params))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # 处理 datetime 和 Decimal 类型
    data = [dict(row) for row in data]  # 转换为字典
    data = serialize_data(data)  # 处理 datetime 和 Decimal

    # 存入 Redis，缓存 60 秒
    redis_client.setex(cache_key, 60, json.dumps(data))

    return data
