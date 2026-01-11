"""
接口参数的结构体定义
"""
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel,Field
class SuiteTypeEnum(str, Enum):
    """
    测试套件类型枚举
    """
    FUNCTIONAL = "功能"
    BUSINESS_FLOW = "业务流"

class SuiteParam(BaseModel):
    """
    测试套件参数结构体
    """
    id: int=Field( description="套件id")
    name: str=Field( description="套件名称")
    create_time: datetime=Field( description="创建时间")
    project_id: int=Field( description="所属项目id")
    modules_id: int|None=Field( description="所属模块id",default=None)
    suite_setup_step: list=Field( description="套件前置步骤",default=[])
    suite_type: SuiteTypeEnum=Field(description="套件类型")

class AddSuiteParam(BaseModel):
    """
    添加测试套件参数结构体
    """
    name: str=Field( description="套件名称")
    project_id: int=Field( description="所属项目id")
    modules_id: int|None=Field( description="所属模块id",default=None)
    suite_setup_step: list=Field( description="套件前置步骤",default=[])
    suite_type: SuiteTypeEnum=Field(description="套件类型")

class UpdateSuiteParam(BaseModel):
    """
    更新测试套件参数结构体
    """

    name: str=Field( description="套件名称")
    modules_id: int|None=Field( description="所属模块id",default=None)
    suite_setup_step: list=Field( description="套件前置步骤",default=[])
    suite_type: SuiteTypeEnum=Field(description="套件类型")

class CasesParam(BaseModel):
    """
    测试用例参数结构体
    """
    id: int=Field( description="用例id")
    name: str=Field( description="用例名称")
    create_time: datetime=Field( description="创建时间")
    project_id: int=Field( description="所属项目id")
    steps: list=Field( description="用例步骤",default=[])

class CaseInfo(CasesParam):
    """
    测试用例信息结构体
    """
    record_total:int=Field( description="执行记录总数")
    state: str=Field( description="最新执行用例状态")
    step_count: int=Field( description="步骤总数")

class CasesListParam(BaseModel):
    """
    测试用例列表参数结构体
    """
    total: int=Field( description="总数")
    page: int=Field( description="页码")
    size: int=Field( description="页大小")
    datas: List[CaseInfo]=Field( description="数据")

class StepParam(BaseModel):
    """
    用例执行步骤参数
    """
    keyword: str=Field( description="关键字"),
    desc:str=Field( description="描述"),
    method:str= Field( description="操作方法"),
    params:dict = Field( description="参数",default={})

class AddCasesParam(BaseModel):
    """
    添加测试用例参数结构体
    """
    name: str=Field( description="用例名称")
    project_id: int=Field( description="所属项目id")
    steps: list[StepParam]| None=Field( description="用例步骤",default=[])

class UpdateCasesParam(BaseModel):
    """
    更新测试用例参数结构体
    """
    name: str|None=Field( description="用例名称",default=None)
    steps: list[StepParam]|None=Field( description="用例步骤",default=[])

class SuiteToCasesParam(BaseModel):
    """
    关联用例和测试套件参数结构体
    """
    id: int=Field( description="关联表id")
    test_suite_id: int=Field( description="套件id")
    test_case_id: int=Field( description="用例id")
    sort: int=Field( description="用例顺序")
    skip: bool=Field( description="跳过",default=False)

class AddSuiteToCasesParam(BaseModel):
    """
    添加关联用例和测试套件参数结构体
    """
    test_case_id: int=Field( description="用例id")
    sort: int=Field( description="用例顺序")

class SuiteToCasesListParam(SuiteToCasesParam):
    """
    关联用例和测试套件列表参数结构体
    """
    test_suite_name: str=Field( description="套件名称")
    test_case_name: str=Field( description="用例名称")

class UpdateSuiteToCasesParam(BaseModel):
    """
    更新关联用例和测试套件参数结构体
    """
    id:int=Field( description="关联表id")
    sort: int=Field( description="用例顺序")