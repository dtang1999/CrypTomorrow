from fastapi import FastAPI, WebSocket
import asyncio
import random
from datetime import datetime

import uvicorn
from api import router

app = FastAPI()

# 注册 API 路由
app.include_router(router)

connections = []


# @app.websocket("/ws/{symbol}")
# async def websocket_endpoint(websocket: WebSocket, symbol: str):
#     """WebSocket 连接，支持订阅不同的币种"""
#     await websocket.accept()
#     connections.append((websocket, symbol))

#     try:
#         while True:
#             # 模拟实时数据（可以改成从 Binance API 获取真实价格）
#             price_data = {
#                 "symbol": symbol,
#                 "timestamp": datetime.utcnow().isoformat(),
#                 "price": round(random.uniform(1000, 5000), 2),
#             }

#             # 只推送给订阅相应币种的客户端
#             for connection, sub_symbol in connections:
#                 if sub_symbol == symbol:
#                     await connection.send_json(price_data)

#             await asyncio.sleep(1)  # 每 1 秒推送一次
#     except:
#         connections.remove((websocket, symbol))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
