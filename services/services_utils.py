import os
from langchain_core.runnables.history import RunnableWithMessageHistory, BaseChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory, ChatMessageHistory
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
import logging
from config import config
from services.event_handler import ChainEvenHandler

services_logger = logging

db_name = "ai_compoiso.db"


def get_chain(llm, prompt, user_id):
    chain = llm
    if prompt:
        chain = prompt | llm
    chain = chain.with_config(callbacks=[ChainEvenHandler(user_id=user_id)])
    return chain


def get_session_history(session_id: str):
    db_path = os.path.join(config.SQLITE3_DB, db_name)
    database_url = f"sqlite:///{db_path}"
    # database_url = "mysql+pymysql://root:hjf123456@127.0.0.1:3306/langchain_db"
    connection = create_engine(database_url)
    chat_history = SQLChatMessageHistory(session_id, connection=connection)
    services_logger.info(f"get_session_history chat_history: {chat_history}")
    return chat_history


def get_history_chain(llm, prompt, user_id, history_messages_key="history"):
    chain = llm
    if prompt:
        chain = prompt | llm
    chain = chain.with_config(callbacks=[ChainEvenHandler(user_id=user_id)])
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        history_messages_key=history_messages_key,
    )
    return chain_with_history


def aget_session_history(session_id: str) -> BaseChatMessageHistory:
    # 使用支持异步操作的 SQLite 驱动程序
    db_path = os.path.join(config.SQLITE3_DB, db_name)
    database_url = f"sqlite+aiosqlite:///{db_path}"
    # database_url = "mysql+aiomysql://root:hjf123456@127.0.0.1:3306/langchain_db"
    async_engine = create_async_engine(database_url)
    # chat_history = SQLChatMessageHistory(session_id, database_url, async_mode=True)
    chat_history = SQLChatMessageHistory(
        session_id, connection=async_engine, async_mode=True)
    services_logger.info(f"aget_session_history chat_history loaded!!!")
    return chat_history


def aget_history_chain(llm, prompt, user_id, history_messages_key="history"):
    chain = llm
    if prompt:
        chain = prompt | llm
    chain = chain.with_config(callbacks=[ChainEvenHandler(user_id=user_id)])
    chain_with_history = RunnableWithMessageHistory(
        chain,
        aget_session_history,
        history_messages_key=history_messages_key,
    )
    return chain_with_history
