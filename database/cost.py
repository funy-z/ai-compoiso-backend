
from sqlalchemy import String, Integer, DateTime, Enum as SqlEnum, Float, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import logging
from enum import Enum
from decimal import Decimal

from database.engine import Base, session, get_utc_plus_8_time


class CurrencyEnum(Enum):
    CNY = "CNY"  # 人民币
    USD = "USD"  # 美元
    EUR = "EUR"  # 欧元
    GBP = "GBP"  # 英镑


class Cost(Base):
    __tablename__ = "cost"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String, nullable=False, comment="调用的用户ID")
    completion_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="响应的token数")
    prompt_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="提问的token数")
    total_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="这一次调用的总token数")
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=4), nullable=False, comment="单价")
    price_tokens: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="单价对应的token数")
    # total_price: Mapped[float] = mapped_column(
    #     Float, nullable=False, comment="总价")
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=15, scale=4), nullable=False, comment="总价")
    currency: Mapped[str] = mapped_column(
        SqlEnum(CurrencyEnum), nullable=False, comment="币种")
    model_provider: Mapped[str] = mapped_column(
        String, nullable=False, comment="模型厂商")
    model_name: Mapped[str] = mapped_column(
        String, nullable=False, comment="模型名称")
    api_key: Mapped[str] = mapped_column(
        String, nullable=True, comment="使用的API_KEY")
    called_time: Mapped[datetime] = mapped_column(
        DateTime, default=get_utc_plus_8_time, comment="调用时间")


def add_cost(cost: Cost):
    session.add(cost)
    try:
        session.commit()  # 提交更改到数据库
    except SQLAlchemyError as e:
        session.rollback()  # 回滚会话，以防止数据库处于不一致状态
        logging.error(f"add_cost error:{str(e)}")
        raise


def query_called_times(user_id: str, query_date: datetime):
    session.query(Cost).filter()
