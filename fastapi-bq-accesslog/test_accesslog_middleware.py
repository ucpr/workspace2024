import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import Request
from starlette.responses import Response
from accesslog_middleware import (
    AccessLogMiddleware,
    log_batch_processor,
    start_log_processing,
    shutdown_processing,
    queue,
    shutdown_event,
)

# pytest-asyncioを使った非同期テスト
@pytest.mark.asyncio
async def test_access_log_middleware_dispatch():
    # モックしたリクエストとレスポンスを準備
    request = MagicMock(Request)
    request.method = "GET"
    request.url.path = "/test"
    request.client.host = "127.0.0.1"
    request.headers = {"user-agent": "test-agent", "content-length": "100"}
    request.query_params = {"param": "value"}

    response = MagicMock(Response)
    response.status_code = 200
    response.headers = {"content-length": "200"}

    # call_nextをモック
    call_next = AsyncMock(return_value=response)

    # ミドルウェアのインスタンスを作成
    middleware = AccessLogMiddleware(app=None)

    # dispatchメソッドの実行
    with patch("time.time", side_effect=[1, 2]):  # 1秒で処理を終わらせるモック
        await middleware.dispatch(request, call_next)

    # キューに1つのログが追加されていることを確認
    assert not queue.empty()
    log_entry = await queue.get()
    assert log_entry["method"] == "GET"
    assert log_entry["path"] == "/test"
    assert log_entry["ip"] == "127.0.0.1"
    assert log_entry["userAgent"] == "test-agent"
    assert log_entry["requestSize"] == 100
    assert log_entry["responseSize"] == 200
    assert log_entry["status"] == 200

@pytest.mark.asyncio
async def test_log_batch_processor():
    # キューにダミーのログエントリを追加
    test_log = {"method": "GET", "path": "/test"}
    await queue.put(test_log)

    # PublisherClientのモックを作成
    with patch("accesslog_middleware.PublisherClient") as mock_publisher:
        mock_publisher_instance = mock_publisher.return_value
        mock_publisher_instance.publish = AsyncMock()

        # バッチプロセッサを非同期で実行
        shutdown_event.clear()
        task = asyncio.create_task(log_batch_processor())

        # バッチ処理が実行され、ログが送信されることを確認
        await asyncio.sleep(0.1)  # 一瞬待つ
        mock_publisher_instance.publish.assert_called_once_with(
            "projects/YOUR_PROJECT_ID/topics/YOUR_TOPIC", [test_log]
        )

        # キューが空になっていることを確認
        assert queue.empty()

        # シャットダウンイベントを発火させてタスクを終了
        shutdown_event.set()
        await task

@pytest.mark.asyncio
async def test_start_log_processing():
    # バッチ処理を開始
    with patch("accesslog_middleware.log_batch_processor") as mock_log_batch_processor:
        mock_task = AsyncMock()
        mock_log_batch_processor.return_value = mock_task
        task = await start_log_processing()

        # タスクが開始されていることを確認
        mock_log_batch_processor.assert_called_once()
        assert isinstance(task, asyncio.Task)

@pytest.mark.asyncio
async def test_shutdown_processing():
    # shutdown_processingのテスト
    task = AsyncMock()

    # shutdown_eventが発火されていることを確認
    await shutdown_processing(task)
    task.assert_called_once()

@pytest.mark.asyncio
async def test_shutdown_processing_with_remaining_queue():
    # キューにログを追加
    test_log = {"method": "GET", "path": "/test"}
    await queue.put(test_log)

    # shutdown_processingを実行
    task = AsyncMock()
    await shutdown_processing(task)

    # キューが空になっていることを確認
    assert queue.empty()
