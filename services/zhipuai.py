# from langchain_community.chat_models import ChatZhipuAI
from custom_langchain.zhipuai import ChatZhipuAI
# from langchain_community.callbacks import get_openai_callback
import os
import logging

from config import config
from services.services_utils import aget_history_chain, get_chain, get_history_chain
os.environ['ZHIPUAI_API_KEY'] = config.ZHIPUAI_API_KEY or ''

model = 'glm-4'

services_logger = logging.getLogger('ai_services')


def invoke(prompt, chain_params, user_id):
    llm = ChatZhipuAI(model=model)
    # chain = llm
    # if prompt:
    #     chain = prompt | llm
    chain = get_chain(llm=llm, prompt=prompt, user_id=user_id)
    result = chain.invoke(chain_params)
    return {"data": result.content}


async def ainvoke(prompt, chain_params, user_id):
    llm = ChatZhipuAI(model=model)
    # chain = llm
    # if prompt:
    #     chain = prompt | llm
    chain = get_chain(llm=llm, prompt=prompt, user_id=user_id)
    result = await chain.ainvoke(chain_params)
    return {"data": result.content}


def stream(prompt, chain_params, user_id):
    llm = ChatZhipuAI(model=model)
    # chain = llm
    # if prompt:
    #     chain = prompt | llm
    chain = get_chain(llm=llm, prompt=prompt, user_id=user_id)
    result = chain.stream(chain_params)
    return result


async def astream(prompt, chain_params, user_id):
    llm = ChatZhipuAI(model=model)
    # chain = llm
    # if prompt:
    #     chain = prompt | llm
    chain = get_chain(llm=llm, prompt=prompt, user_id=user_id)
    services_logger.info(f"zhipuai astream(), prompt: {
                         prompt}, chain_params:{chain_params}")
    result = chain.astream(chain_params)
    return result

# history function ------------------------------------------------------------------------


def invoke_with_history(prompt, chain_params, config, user_id):
    llm = ChatZhipuAI(model=model)
    chain_with_history = get_history_chain(
        llm=llm, prompt=prompt, user_id=user_id)
    services_logger.info(f"zhipuai invoke_with_history(), prompt: {
                         prompt}, chain_params:{chain_params}, config: {config}")
    result = chain_with_history.invoke(chain_params, config)
    services_logger.info(
        f"zhipuai invoke_with_history(), result: {result or '--'}")
    return {"data": result.content}


def stream_with_history(prompt, chain_params, config, user_id):
    llm = ChatZhipuAI(model=model)
    chain_with_history = get_history_chain(
        llm=llm, prompt=prompt, user_id=user_id)

    services_logger.info(f"zhipuai stream_with_history(), prompt: {
                         prompt}, chain_params:{chain_params}, config: {config}")
    result = chain_with_history.stream(chain_params, config)
    services_logger.info(
        f"zhipuai stream_with_history() start to stream response!!!")
    return result


async def ainvoke_with_history(prompt, chain_params, config, user_id):
    llm = ChatZhipuAI(model=model)
    chain_with_history = aget_history_chain(
        llm=llm, prompt=prompt, user_id=user_id)

    services_logger.info(f"zhipuai ainvoke_with_history(), prompt: {
                         prompt}, chain_params:{chain_params}, config: {config}")
    result = await chain_with_history.ainvoke(chain_params, config)
    services_logger.info(
        f"zhipuai ainvoke_with_history(), result:{result or '--'}")
    return {"data": result.content}


async def astream_with_history(prompt, chain_params, config, user_id):
    llm = ChatZhipuAI(model=model)
    chain_with_history = aget_history_chain(
        llm=llm, prompt=prompt, user_id=user_id)

    services_logger.info(f"zhipuai astream_with_history(), prompt: {
                         prompt}, chain_params:{chain_params}, config: {config}")
    result = chain_with_history.astream(chain_params, config)
    services_logger.info(
        f"zhipuai astream_with_history() start to astream response!!!")
    return result
