
import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn
import threading
from uuid import uuid4

import create_tables
from log_config import appLogger
from router import docs, chat
from config import config
from database.user import add_user, query_user


app = FastAPI()
# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    appLogger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error in main"}
    )

app.include_router(docs.router)
app.include_router(chat.router)


# def update_api_key():
#     while True:
#         API_KEY = config.load_api_key()
#         if API_KEY:
#             config.ZHIPUAI_API_KEY = API_KEY
#         else:
#             appLogger.info(
#                 f'monitor ZHIPUAI_API_KEY heartbeat, API_KEY is empty: {API_KEY}')
#         time.sleep(60)  # 每分钟检查一次


# 拦截-中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    user_id = request.cookies.get('ai_compoiso_user_id')
    if not user_id:
        allocation_user_id = uuid4().hex
        appLogger.info(f'allocation user_id and set in headers:'
                       f'{allocation_user_id}')
        request.state.user_id = allocation_user_id
        add_user(user_id=allocation_user_id, ip=request.client.host)
    else:
        user_row = query_user(user_id=user_id)
        if user_row is None:
            add_user(user_id=user_id, ip=request.client.host)
            appLogger.info(f'add exist user_id:{user_id}')
        appLogger.info(f'set user_id in headers:{user_id}')
        request.state.user_id = user_id
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # 请求耗时
    response.headers["X-Process-Time"] = str(process_time)
    # 添加cookie

    # 1天过期,每次访问都更新过期时间
    max_age = 1 * 24 * 60 * 60
    response.set_cookie(key="ai_compoiso_user_id",
                            value=request.state.user_id, max_age=max_age)
    if not user_id:
        appLogger.info(f'set allocation user_id in cookie:{
                       request.state.user_id}')
    else:
        appLogger.info(f'update cookie max_age, cookie:{
                       request.state.user_id}, max_age:{max_age}s')
    return response


@app.get("/")
async def app_root(response: Response, request: Request):
    appLogger.info('visit app_root')
    user_id = request.state.user_id
    appLogger.info(f'receive user_id:{user_id}')
    return {"message": "root path"}

if __name__ == "__main__":
    appLogger.info(f'start app, config: {config}')
    # if config.PRODUCTION_ENV:
    #     threading.Thread(target=update_api_key, daemon=True).start()
    uvicorn.run('main:app', host="0.0.0.0",
                port=config.UVICORN_PORT, reload=config.UVICORN_RELOAD)
