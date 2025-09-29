"""
接口参数的结构体定义
"""
from datetime import datetime

from pydantic import BaseModel,Field

class ProjectParam(BaseModel):
    name: str=Field( description="项目名称")

class ProjectResult(BaseModel):
    """
    返回的项目应答信息
    """
    id: int=Field( description="项目id")
    name: str=Field( description="项目名称")
    crete_time: datetime=Field( description="创建时间"),
    user_info_id: int=Field( description="项目创建者id")