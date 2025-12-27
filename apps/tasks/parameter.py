"""
接口参数的结构体定义
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel,Field

class TaskParam(BaseModel):
    """
    测试任务参数结构体
    """
    id: int=Field( description="任务id")
    name: str=Field( description="任务名称")
    create_time: datetime=Field( description="创建时间")
    project_id: int=Field( description="项目id")

class AddTaskParam(BaseModel):
    """
    添加测试任务参数结构体
    """
    name: str=Field( description="任务名称")
    project_id: int=Field( description="项目id")

class UpdateTaskParam(BaseModel):
    """
    更新测试任务参数结构体
    """
    name: str=Field( description="任务名称")

class TaskSuiteParam(BaseModel):
    """
    任务和测试套件参数结构体
    """
    id: int = Field(description="套件id")
    name: str = Field(description="套件名称")
    create_time: datetime = Field(description="创建时间")
    suite_setup_step: list = Field(description="套件前置步骤", default=[])
    suite_type: str = Field(description="套件类型")

class TaskDetailParam(TaskParam):
    """
    任务和测试套件参数结构体
    """
    suites: List[TaskSuiteParam]=Field( description="测试套件id")