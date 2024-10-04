
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from router import docs

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
    print('visit app_root')
    return {"message": "root path"}

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=80)
