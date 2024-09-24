from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from gcloud.aio.pubsub import PubsubMessage
from gcloud.aio.pubsub import PublisherClient
import fastavro
from fastavro.schema import load_schema
from fastavro.validation import validate

import asyncio
# import aiohttp
import time
import io

BATCH_SIZE = 3
BATCH_INTERVAL = 5
SHUTDOWN_TIMEOUT = 3

app = FastAPI()
queue = asyncio.Queue()
accesslog_schema = load_schema("./schema.avsc")

# session = aiohttp.ClientSession()
pubsub_client = PublisherClient()  # (session=session)
topic = pubsub_client.topic_path('*', 'pybqlog-access-log-v1')


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response: Response = await call_next(request)

        process_time = int((time.time() - start_time) *
                           1_000_000)  # Convert to microseconds
        request_size = request.headers.get("content-length")
        response_size = response.headers.get("content-length")

        # Build the access log entry
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
        # Serialize to Avro
        avro_data = self.serialize_avro(log_entry, accesslog_schema)
        await queue.put(avro_data)

        return response

    def serialize_avro(self, record, schema):
        bytes_writer = io.BytesIO()
        fastavro.schemaless_writer(bytes_writer, schema, record)
        return bytes_writer.getvalue()


async def process_logs():
    batch = []
    while True:
        try:
            log_data = await asyncio.wait_for(
                queue.get(), timeout=BATCH_INTERVAL,
            )
            batch.append(log_data)
            queue.task_done()

            if len(batch) >= BATCH_SIZE:
                await publish_to_pubsub(batch)
                batch = []
        except asyncio.TimeoutError:
            if batch:
                await publish_to_pubsub(batch)
                batch = []
        except asyncio.CancelledError:
            if batch:
                await publish_to_pubsub(batch)
            break


async def publish_to_pubsub(data):
    messages = [
        PubsubMessage(x) for x in data
    ]
    await pubsub_client.publish(topic, messages)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(process_logs())
    yield
    await shutdown()


async def get_remaining_tasks_from_queue(queue: asyncio.Queue) -> list:
    remaining_tasks = []
    while not queue.empty():
        task = await queue.get()
        remaining_tasks.append(task)
        queue.task_done()
    return remaining_tasks


async def shutdown(wait_time: int = 3):
    try:
        await asyncio.wait_for(queue.join(), timeout=SHUTDOWN_TIMEOUT)
    except asyncio.TimeoutError:
        pending_tasks = await get_remaining_tasks_from_queue(queue)
        if pending_tasks:
            for task in pending_tasks:
                task.cancel()
            await asyncio.gather(*pending_tasks, return_exceptions=True)
    # session.close()
    await pubsub_client.close()


app.add_middleware(AccessLogMiddleware)
app.router.lifespan_context = lifespan


@app.get("/")
async def root():
    return {"message": "Hello World"}
