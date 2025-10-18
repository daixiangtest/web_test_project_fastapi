"""
接口参数的结构体定义
"""
from datetime import datetime

from pydantic import BaseModel,Field
from typing import List,Dict
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

class TestEnvParam(BaseModel):
    """
    环境参数结构体
    """
    id: int=Field( description="环境id")
    name: str=Field( description="环境名称")
    create_time: datetime=Field( description="创建时间")
    project_id: int=Field( description="所属项目id")
    host: str=Field( description="环境地址")
    global_vars: dict=Field( description="全局变量",default={})

class AddEnvParam(BaseModel):
    """
    添加环境参数结构体
    """
    name: str=Field( description="环境名称")
    project_id: int=Field( description="所属项目id")
    host: str=Field( description="环境地址")
    global_vars: dict=Field( description="全局变量",default={})

class UpdateEnvParam(BaseModel):
    """
    更新环境参数结构体
    """
    name: str|None=Field( description="环境名称",default=None)
    host: str|None=Field( description="环境地址",default=None)
    global_vars: Dict|None=Field( description="全局变量",default={})

class ProjectModuleParam(BaseModel):
    """
    项目模块参数结构体
    """
    id : int=Field( description="项目模块id")
    name : str=Field( description="项目模块名称")
    project_id : int=Field( description="所属项目id")
    create_time : datetime=Field( description="创建时间")

class AddModuleParam(BaseModel):
    """
    添加项目模块参数结构体
    """
    name : str=Field( description="项目模块名称")
    project_id : int=Field( description="所属项目id")

class UpdateModuleParam(BaseModel):
    """
    更新项目模块参数结构体
    """
    name : str=Field( description="项目模块名称")