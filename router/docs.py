
from fastapi import Body, APIRouter, Request
from typing import Annotated

from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import logging

from custom_types import AIDocBodyType, OpTypeEnum, OpSubTypeEnum
from services import ollama, zhipuai
from config import config

from utils import get_history_config, stream_response, astream_response

router = APIRouter(
    prefix="/ai_docs",
    tags=["ai_docs"],
    responses={404: {"description": "Not found in /ai_docs"}}
)

docs_logger = logging.getLogger('ai_docs')


system_prompt_text = "你是一位著名的作家，名字叫做'费小V'。如果问你'你是谁',请不要回答任何其他内容，直接回答'费小V'即可。现在你的任务是帮助用户将文章的内容进行处理，包括润色、续写文章、缩短文章篇幅或者扩充文章篇幅等等。"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_text),
    MessagesPlaceholder(variable_name="history"),
    # ("human", "请对如下内容进行{action}: '{content}'")
    ("human", "{input}")
])

prompt_free = ChatPromptTemplate.from_messages([
    ("system", system_prompt_text),
    MessagesPlaceholder(variable_name="history"),
    # ("human", '根据用户的问题，对用户的内容进行处理。\
    #  问题="{question}" \
    #  内容="{content}"')
    ("human", "{input}")
])


@router.post("/generate")
async def get_ai_docs(request: Request, params: Annotated[AIDocBodyType, ...] = Body()):
    """
      1. 润色
        1.1 口语化
        1.2 更活泼
        1.3 更正式
      2. 续写
      3. 缩短篇幅
      4. 扩充篇幅
    """
    content = params.content
    question = params.question
    op_type = params.op_type
    op_sub_type = params.op_sub_type
    user_id = request.state.user_id

    docs_logger.info(f"/generate API params, op_type:{op_type}, op_sub_type: {op_sub_type},"
                     f"question: {question},"
                     f"content: {content},"
                     f"user_id: {user_id}")

    exec_prompt = None
    action = ""
    input_msg = ""
    if question:
        # 1. 处理自由问题
        exec_prompt = prompt_free
        if content:
            input_msg = f'根据用户的问题，对用户的内容进行处理。\
                问题="{question}"。 \
                内容="{content}"'
        else:
            input_msg = question
    else:
        # 2. 处理定制问题
        action_dict = {
            "polish": "润色",
            "continue_writing": "续写",
            "shorten": "缩短篇幅",
            "expand": "扩充篇幅",
        }
        sub_action_dict = {
            "colloquial": "更口语化",
            "lively": "更活泼",
            "formal": "更正式",
        }
        if not content:
            return {"success": True, "msg": "content不能为空", "code": 1}
        action = action_dict[op_type]
        if op_type == OpTypeEnum.polish:
            action = f"{action},让内容{
                sub_action_dict[op_sub_type or OpSubTypeEnum.colloquial.value]}"

        input_msg = f"请对如下内容进行{action}: '{content}'"
        exec_prompt = prompt

    result = None
    # chain_params = {
    #     "question": question,
    #     "action": action,
    #     "content": content,
    # }
    chain_params = {
        "input": input_msg,
        "history": [],
    }
    history_config = get_history_config(user_id=user_id)
    docs_logger.info(
        f"/generate API chain_params: {chain_params}, PRODUCTION_ENV: {config.PRODUCTION_ENV}")

    # 1. invoke()
    # if config.PRODUCTION_ENV:
    #     # result = zhipuai.invoke(
    #     #     prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     result = zhipuai.invoke_with_history(
    #         prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, zhipuai astream_with_history start to response! ")
    # else:
    #     # result = ollama.invoke(
    #     #     prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     result = ollama.invoke_with_history(
    #         prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, ollama astream_with_history start to response! ")

    # return result

    # 2. stream()
    # if config.PRODUCTION_ENV:
    #     # result = zhipuai.stream(
    #     #     prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     result = zhipuai.stream_with_history(
    #         prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, zhipuai astream_with_history start to response! ")
    # else:
    #     # result = ollama.stream(prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     result = ollama.stream_with_history(
    #         prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, ollama astream_with_history start to response! ")

    # return StreamingResponse(stream_response(result))

    # 3. ainvoke()
    # if config.PRODUCTION_ENV:
    #     result = await zhipuai.ainvoke(
    #         prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     # result = await zhipuai.ainvoke_with_history(
    #     #     prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, zhipuai astream_with_history start to response! ")
    # else:
    #     # result = await ollama.ainvoke(
    #     #     prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
    #     result = await ollama.ainvoke_with_history(
    #         prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
    #     docs_logger.info(
    #         f"/generate API, ollama astream_with_history start to response! ")

    # return result

    # 4. astream()
    if config.PRODUCTION_ENV:
        # result = await zhipuai.astream(prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
        result = await zhipuai.astream_with_history(prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
        docs_logger.info(
            f"/generate API, zhipuai astream_with_history start to response! ")
    else:
        # result = await ollama.astream(prompt=exec_prompt, chain_params=chain_params, user_id=user_id)
        result = await ollama.astream_with_history(prompt=exec_prompt, chain_params=chain_params, config=history_config, user_id=user_id)
        docs_logger.info(
            f"/generate API, ollama astream_with_history start to response! ")

    return StreamingResponse(astream_response(result))
