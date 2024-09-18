from fastapi import FastAPI, Request, Response
import asyncio

app = FastAPI()


async def publish_to_pubsub(request: Request, response: Response):
    await asyncio.sleep(5)
    print("method", request.method)
    print("url", request.url)
    print("headers", request.headers)
    # print("body", await request.text())
    print("status_code", response.status_code)


async def publish_message(request: Request, response: Response):
    asyncio.create_task(publish_to_pubsub(request, response))


@app.middleware("http")
async def accesslog(request: Request, call_next):
    response = await call_next(request)
    publish_task = asyncio.create_task(publish_message(request, response))
    await asyncio.gather(publish_task)  # publishタスクが完了するまで待つ
    return response


@app.get("/")
async def root():
    print("Hello World")
    return {"message": "Hello World"}
