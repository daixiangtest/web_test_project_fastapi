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

class AddCasesParam(BaseModel):
    """
    添加测试用例参数结构体
    """
    name: str=Field( description="用例名称")
    project_id: int=Field( description="所属项目id")

class UpdateCasesParam(BaseModel):
    """
    更新测试用例参数结构体
    """
    name: str|None=Field( description="用例名称",default=None)
    steps: list|None=Field( description="用例步骤",default=[])

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