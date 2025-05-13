#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# nekoimi 2025/5/12
from fastapi import FastAPI, Request
import uvicorn
import logging

app = FastAPI()

# 设置日志格式和级别
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# 请求中间件，记录详细信息
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 获取请求信息
    client_ip = request.client.host
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    query_params = dict(request.query_params)
    body = await request.body()

    logger.info(f"Request from {client_ip}")
    logger.info(f"Method: {method}")
    logger.info(f"URL: {url}")
    logger.info(f"Headers: {headers}")
    logger.info(f"Query Params: {query_params}")
    logger.info(f"Body: {body.decode('utf-8') if body else 'No body'}")

    response = await call_next(request)
    return response


@app.post("/api/v1/chat/completions")
async def request_endpoint(data: dict):
    return {"message": "Data received", "data": data}


@app.post("/lark/callback")
async def request_endpoint(data: dict):
    return {"message": "Data received", "data": data}


# 主程序入口
if __name__ == "__main__":
    # https://llm-chat.youpin-k8s.net/api/v1
    # http://192.168.0.58:8981/api/v1
    uvicorn.run("main:app", host="0.0.0.0", port=8981, reload=True)
