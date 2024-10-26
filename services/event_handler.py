from uuid import UUID
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult
import logging
from decimal import Decimal, getcontext

from common_info.model_info import model_info
from database.cost import Cost, add_cost
from config import config

# 设置精度(价格计算存在精度问题，使用decimal解决)
getcontext().prec = 10


class ChainEvenHandler(BaseCallbackHandler):
    def __init__(self, user_id: str):
        super().__init__()
        self.user_id = user_id

    def on_llm_end(self,
                   response: LLMResult,
                   *,
                   run_id: UUID,
                   parent_run_id: UUID | None = None,
                   tags: list[str] = None) -> None:
        user_id = self.user_id
        fixed_info = (f"user_id: {user_id}, "
                      f"run_id: {run_id}, parent_run_id: {parent_run_id}, response: {response}.")
        if not response:
            logging.info(f"on_llm_end, {fixed_info}"
                         f"response is None.")
            return
        llm_output = response.llm_output
        # stream()和astream()的token_usage信息放在generations[0][0].generation_info当中
        if (llm_output is None and response.generations
                and response.generations[0] and response.generations[0][0]
                and response.generations[0][0].generation_info):
            llm_output = response.generations[0][0].generation_info
            if not isinstance(llm_output, dict):
                llm_output = dict(llm_output)
        if not llm_output:
            logging.info(f"on_llm_end, llm_output is None. {fixed_info}")
            return
        token_usage = llm_output.get("token_usage", None)
        if not token_usage:
            logging.error(f"on_llm_end, token_usage is None. {fixed_info} ")
            return
        model_name = llm_output.get("model_name", "")
        completion_tokens = token_usage.get('completion_tokens', None)
        prompt_tokens = token_usage.get('prompt_tokens', None)
        total_tokens = token_usage.get('total_tokens', None)
        # 根据token计算花了多少钱
        if not model_name or not completion_tokens or not prompt_tokens or not total_tokens:
            logging.warning(f"on_llm_end, some info is None: "
                            f"model_name: {model_name},"
                            f"completion_tokens:{completion_tokens},"
                            f"prompt_tokens:{prompt_tokens},"
                            f"total_tokens:{total_tokens}."
                            f"{fixed_info}")
            return

        # _model_info: {"provider": "ZhipuAI", "price": 0.1, "price_tokens": 1000}
        _model_info = model_info.get(model_name, None)
        api_key = ''
        if model_name == 'glm-4':
            api_key = config.ZHIPUAI_API_KEY
        if _model_info:
            price_tokens = _model_info.get("price_tokens", 1000)
            total_price = Decimal(total_tokens) / Decimal(price_tokens) * \
                _model_info.get("price", Decimal(0))
            cost = Cost(user_id=user_id,
                        completion_tokens=completion_tokens,
                        prompt_tokens=prompt_tokens,
                        total_tokens=total_tokens,
                        price=_model_info.get("price", Decimal(0)),
                        price_tokens=price_tokens,
                        total_price=total_price,
                        currency=_model_info.get("currency", None),
                        model_provider=_model_info.get("provider"),
                        model_name=model_name,
                        api_key=api_key
                        )
            add_cost(cost=cost)
        else:
            logging.error(f'on_llm_end, _model_info is empty!')

    # async def on_llm_new_token(
    #     self,
    #     token: str,
    #     *,
    #     chunk: GenerationChunk | ChatGenerationChunk = None,
    #     run_id: UUID,
    #     parent_run_id: UUID = None,
    #     tags: list[str] = None,
    #     **kwargs,
    # ) -> None:
    #     ...

    async def on_llm_error(
        self,
        error: BaseException,
        run_id: UUID,
        parent_run_id: UUID = None,
    ) -> None:
        user_id = self.user_id
        logging.error(f"on_llm_error, user_id: {user_id}, run_id: {run_id}, parent_run_id: "
                      f"{parent_run_id}, error: {str(error)}")

    async def on_chain_error(
        self,
        error: BaseException,
        run_id: UUID,
        parent_run_id: UUID = None,
    ) -> None:
        user_id = self.user_id
        logging.error(f"on_chain_error, user_id: {user_id}, run_id: {run_id}, parent_run_id: "
                      f"{parent_run_id}, error: {str(error)}")
