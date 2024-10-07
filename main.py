
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import threading

from log_config import appLogger
from router import docs
from config import config


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

def update_api_key():
    while True:
        API_KEY = config.load_api_key()
        if API_KEY:
            config.ZHIPUAI_API_KEY = API_KEY
        else:  
          appLogger.info(f'monitor ZHIPUAI_API_KEY heartbeat, API_KEY is empty: {API_KEY}')
        time.sleep(60)  # 每分钟检查一次

@app.get("/")
async def app_root():
    appLogger.info('visit app_root')
    return {"message": "root path"}

if __name__ == "__main__":
    appLogger.info(f'start app, config: {config}')
    if config.PRODUCTION_ENV:
        threading.Thread(target=update_api_key, daemon=True).start()
    uvicorn.run('main:app', host="0.0.0.0", port=config.UVICORN_PORT, reload=config.UVICORN_RELOAD)
