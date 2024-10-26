from decimal import Decimal

from database.cost import CurrencyEnum
model_info = {
    "glm-4": {
        "provider": 'ZhipuAI',
        "price": Decimal(0.1),  # 每price_tokens对应的价格
        "price_tokens": 1000,  # 单价token数
        "currency": CurrencyEnum.CNY
    },
    # 本地的llama3模型，价格记为0
    "llama3": {
        "provider": "local",
        "price": Decimal(0),
        "price_tokens": 1000,
        "currency": CurrencyEnum.USD
    },
    "qwen2": {
        "provider": "local",
        "price": Decimal(0),
        "price_tokens": 1000,
        "currency": CurrencyEnum.CNY
    },
}
