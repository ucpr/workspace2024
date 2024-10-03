from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import asyncio

from accesslog_middleware import (
    AccessLogMiddleware,
    start_log_processing,
    shutdown_processing,
)

app = FastAPI()

# Injecting the queue into middleware
app.add_middleware(AccessLogMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_log_processing())
    yield
    await shutdown_processing()


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
    print(f"Domain: {domain} Path: {path} Query Params: {
          query_params} Route: {route}")
    return {"value": "hoge"}
