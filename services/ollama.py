from langchain_community.chat_models import ChatOllama
import logging
from langchain_core.runnables.history import RunnableWithMessageHistory, BaseChatMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory, ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
from sqlalchemy.ext.asyncio import create_async_engine

from .services_utils import aget_history_chain, get_history_chain, get_session_history

model = 'qwen2'

services_logger = logging.getLogger('ai_services')

async def invoke(prompt, chain_params):
  llm = ChatOllama(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = chain.invoke(chain_params)
  return {"data": result.content}

async def ainvoke(prompt, chain_params):
  llm = ChatOllama(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = await chain.ainvoke(chain_params)
  return {"data": result.content}

async def stream(prompt, chain_params):
  llm = ChatOllama(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = chain.stream(chain_params)
  return result

async def astream(prompt, chain_params):
  llm = ChatOllama(model=model)
  chain = llm
  services_logger.info(f"ollama astream(), prompt: {prompt}, chain_params:{chain_params}")
  if prompt:
    chain = prompt | llm
  result = chain.astream(chain_params)
  return result

# history function ------------------------------------------------------------------------

def invoke_with_history(prompt, chain_params, config):
  llm = ChatOllama(model=model)
  chain_with_history = get_history_chain(llm=llm, prompt=prompt)
  services_logger.info(f"ollama invoke_with_history(), prompt: {prompt}, chain_params:{chain_params}, config: {config}")
  result = chain_with_history.invoke(chain_params, config=config)
  services_logger.info(f"ollama invoke_with_history(), result: {result or '--'}")
  return {"data": result.content}

def stream_with_history(prompt, chain_params, config):
  llm = ChatOllama(model=model)
  chain_with_history = get_history_chain(llm=llm, prompt=prompt)

  services_logger.info(f"ollama stream_with_history(), prompt: {prompt}, chain_params:{chain_params}, config: {config}")
  result = chain_with_history.stream(chain_params, config)
  services_logger.info(f"ollama stream_with_history() start to stream response!!!")
  return result

# 异步调用带有历史记录的函数
async def ainvoke_with_history(prompt, chain_params, config):
    llm = ChatOllama(model=model)
    chain_with_history = aget_history_chain(llm=llm, prompt=prompt)
    
    services_logger.info(f"ollama ainvoke_with_history(), prompt: {prompt}, chain_params:{chain_params}, config: {config}")
    result = await chain_with_history.ainvoke(chain_params, config)
    services_logger.info(f"ollama ainvoke_with_history(), result:{result or '--'}")
    return {"data": result.content}

async def astream_with_history(prompt, chain_params, config):
  llm = ChatOllama(model=model)
  chain_with_history = aget_history_chain(llm=llm, prompt=prompt)

  services_logger.info(f"ollama astream_with_history(), prompt: {prompt}, chain_params:{chain_params}, config: {config}")
  result = chain_with_history.astream(chain_params, config)
  services_logger.info(f"ollama astream_with_history() start to astream response!!!")
  return result

def invoke_with_history_text(prompt, chain_params, config):
  llm = ChatOllama(model=model)
  # chain_with_history = get_history_chain(llm=llm, prompt=prompt)
  chain_with_history = RunnableWithMessageHistory(
    llm,
    get_session_history,
  )
  services_logger.info(f"ollama invoke_with_history(), prompt: {prompt}, chain_params:{chain_params}, config: {config}")
  result = chain_with_history.invoke(chain_params, config=config)
  services_logger.info(f"ollama invoke_with_history(), result: {result or '--'}")
  return {"data": result.content}
