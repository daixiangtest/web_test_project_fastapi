"""
接口参数的结构体定义
"""
from datetime import datetime

from pydantic import BaseModel,Field

class CornTabParam(BaseModel):
    """
    创建定时任务参数
    """
    minute: str=Field(...,description="分钟")
    hour: str=Field(...,description="小时")
    day: str=Field(...,description="天")
    month: str=Field(...,description="月")
    day_of_week: str=Field(...,description="星期")

class CornParam(BaseModel):
    """
    创建定时任务参数
    """
    name:str=Field(description="任务名称")
    project_id: int=Field(description="项目id")
    env_id:int= Field(description="环境id")
    task_id:int= Field(description="任务id")
    state:bool= Field(description="任务状态")
    run_type:str= Field(description="运行方式")
    interval: int|None=Field(description="定时任务间隔时间", default=60)
    date:datetime|None= Field(description="定时配置时间", default=None)
    crontab: CornTabParam|None=Field(description="周期任务配置参数", default=None)

class CornUpdateParam(BaseModel):
    """
    更新定时任务参数
    """
    name:str|None=Field(description="任务名称", default=None)
    run_type:str= Field(description="运行方式")
    interval: int|None=Field(description="定时任务间隔时间", default=60)
    date:datetime|None= Field(description="定时配置时间", default=None)
    crontab: CornTabParam|None=Field(description="周期任务配置参数", default=None)