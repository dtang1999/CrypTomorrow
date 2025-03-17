import psycopg2

# 配置 PostgreSQL 连接信息
DB_NAME = "crypto_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"  # 如果 PostgreSQL 运行在本机
DB_PORT = "5432"  # 默认端口

try:
    # 连接到 PostgreSQL 数据库
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    
    # 创建游标对象
    cur = conn.cursor()
    
    # 执行 SQL 查询
    cur.execute("SELECT version();")
    
    # 获取查询结果
    pg_version = cur.fetchone()
    
    print(f"成功连接到 PostgreSQL，版本信息: {pg_version[0]}")
    
    # 关闭游标和连接
    cur.close()
    conn.close()

except Exception as e:
    print(f"数据库连接失败: {e}")
