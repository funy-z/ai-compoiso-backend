
from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
import logging

from database.engine import Base, session, get_utc_plus_8_time


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(
        String, nullable=False, comment="用户ID")
    user_name: Mapped[str] = mapped_column(
        String(300), nullable=True, comment="用户名")
    ip: Mapped[str] = mapped_column(String, nullable=True, comment="用户的IP地址")
    telephone: Mapped[str] = mapped_column(
        String, nullable=True, comment="手机号码")
    create_time: Mapped[datetime] = mapped_column(
        DateTime, default=get_utc_plus_8_time, comment="注册时间")


# 添加用户
def add_user(user_id: str, ip: str = ""):
    user = User(user_id=user_id, ip=ip)
    session.add(user)
    try:
        session.commit()  # 提交更改到数据库
    except SQLAlchemyError as e:
        session.rollback()  # 回滚会话，以防止数据库处于不一致状态
        logging.error(f"add_user error:{str(e)}")
        raise


# 根据user_id查询用户
def query_user(user_id: str):
    try:
        query = session.query(User).filter_by(user_id=user_id)
        result = query.one()
        return result
    except NoResultFound:
        # 处理没有找到记录的情况
        print(f"No user found with user_id: {user_id}")
        return None


# 查询用户列表
def query_users(keyword: str, page_index: int = 0, page_size: int = 10):
    if keyword:
        query = session.query(User).filter(User.user_name.like(f"%{keyword}%"))
    else:
        query = session.query(User)

    # 分页
    offset = page_index * page_size
    query = query.offset(offset).limit(page_size)

    result = query.all()
    return result
