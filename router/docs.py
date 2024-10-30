
from fastapi import Body, APIRouter, Request
from typing import Annotated

from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import logging

from custom_types import AIDocBodyType, OpTypeEnum, OpSubTypeEnum
from services import chat_models
from config import config
from services.chat_models import AICompoisoModelServiceType, ModelProviderEnum

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
    ("human", "{input}")
])

prompt_free = ChatPromptTemplate.from_messages([
    ("system", system_prompt_text),
    MessagesPlaceholder(variable_name="history"),
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
    chain_params = {
        "input": input_msg,
        "history": [],
    }
    history_config = get_history_config(user_id=user_id)
    docs_logger.info(
        f"/generate API chain_params: {chain_params}, PRODUCTION_ENV: {config.PRODUCTION_ENV}")
    # 整合调用 start ----------------------------------------------------------------------------
    # model_provider = ModelProviderEnum.zhipuAI if config.PRODUCTION_ENV else ModelProviderEnum.ollama
    if params.model_provider:
        try:
            model_provider = ModelProviderEnum[params.model_provider]
        except KeyError as e:
            msg = f"Invalid model provider: {
                params.model_provider}, error: {str(e)}"
            logging.error(msg)
            return {"success": False, "msg": msg}
    else:
        model_provider = ModelProviderEnum.zhipuAI if config.PRODUCTION_ENV else ModelProviderEnum.ollama
    chat_model_params = AICompoisoModelServiceType(prompt=exec_prompt,
                                                   chain_params=chain_params,
                                                   user_id=user_id,
                                                   model_provider=model_provider,
                                                   model_name=params.model_name,
                                                   with_history=True,
                                                   config=history_config)
    # 1. invoke()
    # result = chat_models.invoke(chat_model_params)
    # return result

    # # 2. stream()
    # result = chat_models.stream(chat_model_params)
    # return StreamingResponse(stream_response(result))

    # 3. ainvoke()
    # result = await chat_models.ainvoke(chat_model_params)
    # return result

    # 4. astream()
    result = await chat_models.astream(chat_model_params)
    return StreamingResponse(astream_response(result))
    # 整合调用 end ----------------------------------------------------------------------------
