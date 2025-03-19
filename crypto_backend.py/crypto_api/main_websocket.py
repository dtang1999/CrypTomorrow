from fastapi import FastAPI, WebSocket
import asyncio
import random
from datetime import datetime

app = FastAPI()

# 连接的 WebSocket 客户端
connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 连接，实时推送最新价格"""
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            # 模拟实时价格数据（可以改成从 Binance API 获取最新价格）
            price_data = {
                "symbol": "BTCUSDT",
                "timestamp": datetime.utcnow().isoformat(),
                "price": round(random.uniform(45000, 46000), 2)
            }
            
            # 发送数据给所有客户端
            for connection in connections:
                await connection.send_json(price_data)
            
            await asyncio.sleep(1)  # 每 1 秒推送一次
    except:
        connections.remove(websocket)
