import pytest
import asyncio
import time
from fastapi import FastAPI
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from accesslog_middleware import AccessLogMiddleware, log_batch_processor, shutdown_processing, queue, shutdown_event

@pytest.fixture
def test_app():
    app = FastAPI()
    app.add_middleware(AccessLogMiddleware)
    return app

@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)

@pytest.mark.asyncio
async def test_access_log_middleware(test_app):
    # テスト用のリクエストを行い、ミドルウェアの動作を確認
    with TestClient(test_app) as client:
        response = client.get("/some-endpoint")
        assert response.status_code == 404  # テストではエンドポイントがないため404を想定

    # キューにログが追加されていることを確認
    log_entry = await queue.get()
    assert log_entry["method"] == "GET"
    assert log_entry["status"] == 404
    assert "duration" in log_entry


@pytest.mark.asyncio
async def test_shutdown_processing():
    # キューにアイテムを追加
    await queue.put({"message": "shutdown log"})
    
    task = asyncio.create_task(log_batch_processor())

    # シャットダウン処理のテスト
    await shutdown_processing(task)

    # キューが空であることを確認
    assert queue.empty()
