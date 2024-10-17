from fastapi import Body, APIRouter, Request
import logging
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

from services import ollama, zhipuai
from config import config
from utils import astream_response, get_history_config, stream_response

chat_logger = logging.getLogger('ai_chat')

router = APIRouter(
    prefix="/ai_chat",
    tags=["ai_chat"],
    responses={404: {"description": "Not found in /ai_chat"}}
)

system_prompt_text = "你是一位著名的作家，名字叫做'费小V'。如果问你'你是谁',请不要回答任何其他内容，直接回答'费小V'即可。"
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt_text),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

@router.post("/chat_with_history")
async def chat_with_history(request: Request, message: str = Body(...)):
    user_id = request.state.user_id
    chat_logger.info(f"/chat_with_history API, user_id: {user_id}, message:{message}")
    # result = ollama.invoke_with_history(params, config={"configurable": {"session_id": user_id}})
    # return { "data": result }
    chain_params = {
        "input": message,
    }
    history_config = get_history_config(user_id=user_id)
    if config.PRODUCTION_ENV:
        # result = zhipuai.invoke_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        # result = zhipuai.stream_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        # result = await zhipuai.ainvoke_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        result = await zhipuai.astream_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        chat_logger.info(f"/chat_with_history API, zhipuai invoke_with_history result:{result}")
    else:
        # result = ollama.invoke_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        # result = ollama.stream_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        # result = await ollama.ainvoke_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        result = await ollama.astream_with_history(prompt=prompt, chain_params=chain_params, config=history_config)
        chat_logger.info(f"/chat_with_history API, ollama invoke_with_history result:{result}")
    # 1. invoke() return
    # return result
    # 2. stream() return
    # return StreamingResponse(stream_response(result))
    # 3. ainvoke() return
    # return result
    # 4. astream() return
    return StreamingResponse(astream_response(result))

