from langchain_community.chat_models import ChatOllama
import logging

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
