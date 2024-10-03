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


BATCH_SIZE = 100
BATCH_INTERVAL = 3
SHUTDOWN_TIMEOUT = 10

# session = aiohttp.ClientSession()
# pubsub_client = PublisherClient(session=session)
# topic = pubsub_client.topic_path('*', 'pybqlog-access-log-v1')

queue: asyncio.Queue = asyncio.Queue()


class AccessLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response: Response = await call_next(request)

        process_time = int((time.time() - start_time) *
                           1_000_000)  # Convert to microseconds
        request_size = request.headers.get("content-length")
        response_size = response.headers.get("content-length")

        log_entry = {
            u"timestamp": int(time.time() * 1_000_000),
            u"id": None,
            u"traceId": None,
            u"ip": request.client.host,
            u"userAgent": request.headers.get("user-agent"),
            u"method": request.method,
            u"path": request.url.path,
            u"query": request.url.query,
            u"status": response.status_code,
            u"duration": process_time,
            u"requestSize": int(request_size) if request_size else None,
            u"responseSize": int(response_size) if response_size else None,
        }

        if not validate(log_entry, accesslog_schema):
            return response

        avro_data = self.serialize_avro(log_entry, accesslog_schema)
        await queue.put(avro_data)

        return response

    def serialize_avro(self, record, schema):
        bytes_writer = io.BytesIO()
        fastavro.schemaless_writer(bytes_writer, schema, record)
        return bytes_writer.getvalue()


async def start_log_processing():
    batch = []
    async with aiohttp.ClientSession() as session:
        pubsub_client = PublisherClient(session=session)
        topic = pubsub_client.topic_path('*', 'pybqlog-access-log-v1')

        while True:
            try:
                log_data = await asyncio.wait_for(queue.get(), timeout=BATCH_INTERVAL)
                batch.append(log_data)
                queue.task_done()

                if len(batch) >= BATCH_SIZE:
                    await publish_to_pubsub(batch, pubsub_client, topic)
                    batch = []
            except asyncio.TimeoutError:
                if batch:
                    await publish_to_pubsub(batch, pubsub_client, topic)
                    batch = []
            except asyncio.CancelledError:
                if batch:
                    await publish_to_pubsub(batch, pubsub_client, topic)
                break


async def publish_to_pubsub(data, pubsub_client, topic):
    messages = [PubsubMessage(x) for x in data]
    # await pubsub_client.publish(topic, messages)
    await asyncio.sleep(1)
    print(f"Published {len(messages)} messages to Pub/Sub")


async def shutdown_processing():
    try:
        await asyncio.wait_for(queue.join(), timeout=SHUTDOWN_TIMEOUT)
        print("All tasks are done")
    except asyncio.TimeoutError:
        remaining_tasks = await get_remaining_tasks_from_queue()
        for task in remaining_tasks:
            task.cancel()
        await asyncio.gather(*remaining_tasks, return_exceptions=True)


async def get_remaining_tasks_from_queue() -> list:
    remaining_tasks = []
    while not queue.empty():
        task = await queue.get()
        remaining_tasks.append(task)
        queue.task_done()
    return remaining_tasks
