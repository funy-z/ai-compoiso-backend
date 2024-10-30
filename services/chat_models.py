import os
import logging
from pydantic import BaseModel, Field
from typing import Any
from enum import Enum

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from custom_langchain.zhipuai import ChatZhipuAI
from config import config
from services.services_utils import aget_history_chain, get_chain, get_history_chain


class ModelProviderEnum(Enum):
    openAI = "openAI"
    ollama = "ollama"
    zhipuAI = "zhipuAI"


API_KEY_INFO = {
    ModelProviderEnum.openAI: "OPENAI_API_KEY",
    ModelProviderEnum.zhipuAI: "ZHIPUAI_API_KEY"
}


class AICompoisoModelServiceType(BaseModel):
    prompt: ChatPromptTemplate
    chain_params: dict[str, Any]
    user_id: str
    model_provider: ModelProviderEnum
    model_name: str = Field(default="")
    with_history: bool = Field(default=True)
    config: Any = Field(default=None)


def load_api_key(file_name: str):
    try:
        dir_path = config.API_KEY_DIR
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, "r") as file:
            result = file.read().strip()
            logging.info(f"open {file_path}, result: {result}")
            return result
    except FileNotFoundError as e:
        logging.error(f"read {file_path} failed, {str(e)}")
        return None


def set_aip_key(model_provider: ModelProviderEnum):
    # os.environ["ZHIPUAI_API_KEY"] = load_api_key("ZHIPUAI_API_KEY")
    api_key_name = API_KEY_INFO.get(model_provider, None)
    if not api_key_name:
        logging.warning(f"model_provider: {model_provider}, "
                        "API_KEY_INFO is empty")
        return
    if os.environ.get(api_key_name, None) is None:
        api_key_value = load_api_key(api_key_name)
        if not api_key_value:
            raise Exception(
                f"api_key_value is empty, api_key_name: {api_key_name}")
        os.environ[api_key_name] = api_key_value


def create_llm(model_provider: ModelProviderEnum, model_name: str):
    set_aip_key(model_provider)
    if model_provider == ModelProviderEnum.openAI:
        llm = ChatOpenAI(model=model_name or "gpt-4",
                         openai_api_base="https://api.openai-hk.com/v1/")
    elif model_provider == ModelProviderEnum.zhipuAI:
        llm = ChatZhipuAI(model=model_name or "glm-4")
    else:
        llm = ChatOllama(model=model_name or "llama3")
    return llm


def invoke(params: AICompoisoModelServiceType):

    llm = create_llm(params.model_provider, params.model_name)

    if params.with_history:
        chain = get_history_chain(
            llm=llm, prompt=params.prompt, user_id=params.user_id)
    else:
        chain = get_chain(llm=llm, prompt=params.prompt,
                          user_id=params.user_id)

    result = chain.invoke(params.chain_params, params.config)
    return {"data": result.content}


def stream(params: AICompoisoModelServiceType):

    llm = create_llm(params.model_provider, params.model_name)

    if params.with_history:
        chain = get_history_chain(
            llm=llm, prompt=params.prompt, user_id=params.user_id)
    else:
        chain = get_chain(llm=llm, prompt=params.prompt,
                          user_id=params.user_id)

    result = chain.stream(params.chain_params, params.config)
    return result


async def ainvoke(params: AICompoisoModelServiceType):

    llm = create_llm(params.model_provider, params.model_name)

    if params.with_history:
        chain = aget_history_chain(
            llm=llm, prompt=params.prompt, user_id=params.user_id)
    else:
        chain = get_chain(llm=llm, prompt=params.prompt,
                          user_id=params.user_id)

    result = await chain.ainvoke(params.chain_params, params.config)
    return {"data": result.content}


async def astream(params: AICompoisoModelServiceType):

    llm = create_llm(params.model_provider, params.model_name)

    if params.with_history:
        chain = aget_history_chain(
            llm=llm, prompt=params.prompt, user_id=params.user_id)
    else:
        chain = get_chain(llm=llm, prompt=params.prompt,
                          user_id=params.user_id)

    result = chain.astream(params.chain_params, params.config)
    return result
