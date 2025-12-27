"""
接口参数的结构体定义
"""
from datetime import datetime

from pydantic import BaseModel,Field

class RunCaseParam(BaseModel):
    """
    运行用例参数
    """
    env_id:int=Field(description="环境id")
    browser_type:str|None=Field(description="浏览器类型",default="chrome")
    device_id:str|None=Field(description="设备id",default="")

class CaseResulParam(BaseModel):
    """
    用例结果参数
    """
    id: int = Field(description="用例结果id")
    case_id: int = Field(description="用例id")
    case_name: str=Field(description="用例名称")
    suite_record_id: int=Field(description="用例集执行记录id")
    status : str=Field(description="用例执行状态")
    run_info: dict=Field(description="用例执行信息")

class SuiteResulParam(BaseModel):
    """
    用例结果参数
    """
    id: int=Field(description="用例集结果id")
    suite_id: int=Field(description="用例集id")
    suite_name: str=Field(description="用例集名称")
    env:dict=Field(description="环境信息")
    status: str=Field(description="用例集执行状态")
    all: int=Field(description="用例集总用例数")
    success: int=Field(description="用例集成功用例数")
    fail: int=Field(description="用例集失败用例数")
    error: int=Field(description="用例集错误用例数")
    no_run: int=Field(description="用例集未执行用例数")
    skip:int=Field(description="用例集跳过用例数")
    duration:float=Field(description="用例集执行时长")
    pass_rate:float=Field(description="用例集通过率")
    suite_log:list=Field(description="用例集日志")
    task_record_id: int=Field(description="任务执行记录id")

class TaskResulParam(BaseModel):
    """
    用例结果参数
    """
    id: int=Field(description="任务结果id")
    project_id: int=Field(description="项目id")
    task_id: int=Field(description="任务id")
    task_name: str=Field(description="任务名称")
    env: dict
    start_time: datetime=Field(description="任务开始时间")
    status: str=Field(description="任务执行状态")
    all: int=Field(description="总用例数")
    run_all: int=Field(description="运行的总用例数")
    success: int=Field(description="成功用例数")
    skip: int=Field(description="跳过用例数")
    no_run: int=Field(description="未执行用例数")
    error: int=Field(description="错误用例数")
    fail: int=Field(description="失败用例数")


