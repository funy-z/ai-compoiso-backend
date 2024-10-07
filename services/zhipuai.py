from langchain_community.chat_models import ChatZhipuAI
import os
import logging

from config import config
os.environ['ZHIPUAI_API_KEY'] = config.ZHIPUAI_API_KEY or ''

model = 'glm-4'

services_logger = logging.getLogger('ai_services')

async def invoke(prompt, chain_params):
  llm = ChatZhipuAI(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = chain.invoke(chain_params)
  return {"data": result.content}

async def ainvoke(prompt, chain_params):
  llm = ChatZhipuAI(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = await chain.ainvoke(chain_params)
  return {"data": result.content}

async def stream(prompt, chain_params):
  llm = ChatZhipuAI(model=model)
  chain = llm
  if prompt:
    chain = prompt | llm
  result = chain.stream(chain_params)
  return result

async def astream(prompt, chain_params):
  llm = ChatZhipuAI(model=model)
  chain = llm
  services_logger.info(f"zhipuai astream(), prompt: {prompt}, chain_params:{chain_params}")
  if prompt:
    chain = prompt | llm
  result = chain.astream(chain_params)
  return result
