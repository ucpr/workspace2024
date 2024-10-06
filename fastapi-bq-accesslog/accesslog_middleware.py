import time
import io
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import fastavro
from fastavro.validation import validate
from schema import accesslog_schema
import asyncio
from gcloud.aio.pubsub import PubsubMessage, PublisherClient
import aiohttp
import logging
import os

# 環境変数から設定値を取得
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))
BATCH_INTERVAL = int(os.getenv("BATCH_INTERVAL", 10))
SHUTDOWN_TIMEOUT = int(os.getenv("SHUTDOWN_TIMEOUT", 10))


# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

queue: asyncio.Queue = asyncio.Queue()
shutdown_event = asyncio.Event()

class AccessLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response: Response = await call_next(request)

        process_time = int((time.time() - start_time) * 1_000_000)  # マイクロ秒に変換
        request_size = request.headers.get("content-length")
        response_size = response.headers.get("content-length")

        log_entry = {
            "timestamp": int(time.time() * 1_000_000),
            "id": None,
            "traceId": None,
            "ip": request.client.host,
            "userAgent": request.headers.get("user-agent"),
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params),
            "status": response.status_code,
            "duration": process_time,
            "requestSize": int(request_size) if request_size else None,
            "responseSize": int(response_size) if response_size else None,
        }

        # Avroのバリデーションを追加
        if validate(log_entry, accesslog_schema):
            await queue.put(log_entry)
        else:
            logger.error("Log entry validation failed")

        return response


async def start_log_processing():
    # バッチ処理をバックグラウンドで実行
    logger.info("Starting log processing")
    task = asyncio.create_task(log_batch_processor())
    return task


async def log_batch_processor():
    publisher = PublisherClient()
    while not shutdown_event.is_set() or not queue.empty():
        try:
            # キューに残っているログをバッチ処理
            batch_size = min(queue.qsize(), BATCH_SIZE)
            batch = [await queue.get() for _ in range(batch_size)]
            if batch:
                # ログの送信処理
                # await publisher.publish("projects/YOUR_PROJECT_ID/topics/YOUR_TOPIC", batch)
                await asyncio.sleep(1)
                logger.info(f"Published batch of {len(batch)} log entries")
            await asyncio.sleep(BATCH_INTERVAL)
        except Exception as e:
            logger.error(f"Error in log batch processor: {e}")


async def shutdown_processing(task):
    # シャットダウンイベントをセット
    shutdown_event.set()

    # キューが空になるまでバッチ処理を継続
    try:
        await asyncio.wait_for(task, SHUTDOWN_TIMEOUT)
    except asyncio.TimeoutError:
        logger.error("Shutdown timeout reached")
    
    # キューに残っているアイテムを全て処理
    while not queue.empty():
        logger.info("Processing remaining log entries before shutdown...")
        await log_batch_processor()
