import os
from sqlalchemy import create_engine, String, INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session
from datetime import datetime
from zoneinfo import ZoneInfo

from config import config

db_name = "ai_compoiso.db"
db_path = os.path.join(config.SQLITE3_DB, db_name)

engine = create_engine(f"sqlite:///{db_path}", echo=True)

Session = sessionmaker(bind=engine)

session = Session()


class Base(DeclarativeBase):
    ...


# 获取当前时间并转换为 UTC+8(北京时间)
def get_utc_plus_8_time():
    current_time = datetime.now()
    utc_time = current_time.astimezone(ZoneInfo("UTC"))
    peking_time = utc_time.astimezone(ZoneInfo("Asia/Shanghai"))
    return peking_time
