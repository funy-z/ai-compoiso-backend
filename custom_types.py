from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field


class OpTypeEnum(Enum):
    polish = "polish"
    continue_writing = "continue_writing"
    shorten = "shorten"
    expand = "expand"


class OpSubTypeEnum(Enum):
    colloquial = "colloquial"
    lively = "lively"
    formal = "formal"


class AIDocBodyType(BaseModel):
    content: Annotated[str, "文章内容"] = ""
    question: Annotated[str, "自由问题"]
    # 整合
    op_type: Annotated[OpTypeEnum | str,
                       "操作类型:润色/续写/缩短篇幅/扩充篇幅"] = Field(default="")
    op_sub_type: Annotated[OpSubTypeEnum | str, "润色的子类型"] = Field(
        default="")
    model_provider: str = Field(default="")
    model_name: str = Field(default="")
