
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .router import docs

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

app.include_router(docs.router)


@app.get("/")
async def app_root():
    return {"message": "root path"}
