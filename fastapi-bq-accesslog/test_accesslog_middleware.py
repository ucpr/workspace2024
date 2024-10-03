import pytest
from starlette.responses import Response
from accesslog_middleware import AccessLogMiddleware, start_log_processing, publish_to_pubsub, get_remaining_tasks_from_queue, shutdown_processing
from fastapi import FastAPI
import asyncio


@pytest.fixture
def queue():
    return asyncio.Queue()


@pytest.fixture
def app(queue):
    app = FastAPI()
    app.add_middleware(AccessLogMiddleware, queue=queue)
    return app


@pytest.fixture
def middleware(queue):
    return AccessLogMiddleware(app=None, queue=queue)


@pytest.mark.asyncio
async def test_access_log_middleware(middleware, queue):
    class MockRequest:
        client = type("Client", (), {"host": "127.0.0.1"})
        headers = {"user-agent": "test-agent", "content-length": "1024"}
        method = "GET"
        url = type("URL", (), {"path": "/test", "query": "param=value"})

    request = MockRequest()
    response = Response()

    async def mock_call_next(request):
        return response  # Simulate the response from call_next

    # Pass the asynchronous call_next
    await middleware.dispatch(request, mock_call_next)

    assert not queue.empty()
    avro_data = await queue.get()
    assert avro_data is not None


@pytest.mark.asyncio
async def test_publish_to_pubsub(monkeypatch):
    class MockPublisherClient:
        async def publish(self, topic, messages):
            assert len(messages) > 0
            assert messages[0] is not None

    pubsub_client = MockPublisherClient()
    topic = "mock_topic"

    data = [b"test-avro-data"]
    await publish_to_pubsub(data, pubsub_client, topic)


@pytest.mark.asyncio
async def test_start_log_processing(queue, monkeypatch):
    class MockPublisherClient:
        async def publish(self, topic, messages):
            assert len(messages) == 1
            assert messages[0] is not None

        async def topic_path(self, *args, **kwargs):
            return "mock_topic_path"

    async def mock_client_session(*args, **kwargs):
        return MockPublisherClient()

    # Correct the monkeypatch to replace the PublisherClient
    # instantiation properly
    monkeypatch.setattr("accesslog_middleware.PublisherClient",
                        lambda *args, **kwargs: MockPublisherClient())

    # Add an item to the queue
    await queue.put(b"test-avro-data")

    # Run the processing task
    processing_task = asyncio.create_task(start_log_processing(queue))

    # Let the processing task run briefly
    await asyncio.sleep(1)

    # Cancel the processing task
    processing_task.cancel()
    try:
        await processing_task
    except asyncio.CancelledError:
        pass  # Expected behavior

@pytest.mark.asyncio
async def test_get_remaining_tasks_from_queue():
    queue = asyncio.Queue()

    # Put test data into the queue
    test_data = [b"test1", b"test2", b"test3"]
    for data in test_data:
        await queue.put(data)

    remaining_tasks = await get_remaining_tasks_from_queue(queue)

    assert remaining_tasks == test_data
    assert queue.empty()  # Ensure the queue is empty after retrieving tasks


@pytest.mark.asyncio
async def test_shutdown_processing(monkeypatch):
    class MockPublisherClient:
        async def publish(self, topic, messages):
            pass  # Mock implementation does nothing

        async def close(self):
            pass  # Mock close does nothing

    # Mock the PublisherClient to prevent real pubsub interaction
    monkeypatch.setattr("accesslog_middleware.PublisherClient", MockPublisherClient)

    queue = asyncio.Queue()
    
    # Adding test data to the queue
    await queue.put(b"test-avro-data")
    await queue.put(b"another-test-data")

    async def mock_process_logs():
        # This simulates processing the queue items, calling task_done for each item
        while not queue.empty():
            await queue.get()
            queue.task_done()

    # Start a mock task to simulate processing logs
    process_task = asyncio.create_task(mock_process_logs())

    # Call the shutdown_processing function
    await shutdown_processing(queue)

    # Wait for the mock processing task to finish
    await process_task

    # Verify that the queue is now empty
    assert queue.empty()