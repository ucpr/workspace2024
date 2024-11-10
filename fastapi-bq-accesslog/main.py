from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import asyncio
import logging
from accesslog_middleware import (
    AccessLogMiddleware,
    start_log_processing,
    shutdown_processing,
)

# ロギング設定
logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# ミドルウェアにキューを注入
app.add_middleware(AccessLogMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 例外処理を追加し、エラー時にログを出力
    try:
        task = asyncio.create_task(start_log_processing())
        yield
    except Exception as e:
        logger.error(f"Error in lifespan context: {e}")
    finally:
        await shutdown_processing(task)


app.router.lifespan_context = lifespan


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test/{value}")
async def test(request: Request):
    domain = request.base_url
    path = request.url.path
    route = request.scope['root_path'] + request.scope['route'].path
    query_params = request.query_params
    print(request.client)
    logger.info(f"Domain: {domain} Path: {path} Query Params: {query_params} Route: {route}")
    return {"value": "hoge"}
