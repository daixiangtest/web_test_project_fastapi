"""接口函数定义"""

from fastapi import APIRouter, HTTPException, Depends

from apps.projects.models import TestProject, ProjectModule
from apps.users.models import Users
from comms.auth import is_authenticated
from apps.cases.parameter import SuiteParam, AddSuiteParam, UpdateSuiteParam, CasesParam, AddCasesParam, \
    UpdateCasesParam, SuiteToCasesParam, AddSuiteToCasesParam, SuiteToCasesListParam, UpdateSuiteToCasesParam
from apps.cases.models import TestCases, TestSuites, SuiteToCase

# 路由注册添加依赖项中添加用户权限校验
test_router=APIRouter(prefix="/api/test",tags=["测试套件的管理"],dependencies=[Depends(is_authenticated)])

@test_router.post("/suite",response_model=SuiteParam,description="添加测试套件")
async def add_suite(suite:AddSuiteParam):
    """
    添加测试套件
    :param suite: 测试套件参数
    :param user: 当前用户
    :return: 添加的测试套件信息
    """
    project=await TestProject.get_or_none(id=suite.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    if suite.modules_id:
        modules=await ProjectModule.get_or_none(id=suite.modules_id)
        if not modules:
            raise HTTPException(status_code=404, detail="模块不存在")
    # 添加测试套件
    suite_obj=await TestSuites.create(name=suite.name,project_id=suite.project_id,modules_id=suite.modules_id,
                                      suite_setup_step=suite.suite_setup_step,suite_type=suite.suite_type)
    return SuiteParam(**suite_obj.__dict__)

@test_router.get("/suite",response_model=list[SuiteParam],description="获取测试套件列表")
async def get_suite(project_id:int|None=None,modules_id:int|None=None):
    """
    获取测试套件列表
    :param modules_id: 模块id
    :param project_id: 项目id
    :param user: 当前用户
    :return: 测试套件列表
    """
    que=TestSuites.all()
    project=await TestProject.get_or_none(id=project_id)
    modules=await ProjectModule.get_or_none(id=modules_id)
    if project:
        que=que.filter(project_id=project_id)
    if modules:
        que=que.filter(modules_id=modules_id)
    suites=await que.all()
    return suites

@test_router.get("/suite/{suite_id}",response_model=SuiteParam,description="获取测试套件详情")
async def get_suite_detail(suite_id:int):
    """
    获取测试套件详情
    :param suite_id: 测试套件id
    :param user: 当前用户
    :return: 测试套件详情
    """
    suite=await TestSuites.get_or_none(id=suite_id)
    if not suite:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    return SuiteParam(**suite.__dict__)

@test_router.put("/suite/{suite_id}",response_model=SuiteParam,description="更新测试套件")
async def update_suite(suite_id:int,suite:UpdateSuiteParam):
    """
    更新测试套件
    :param suite_id: 测试套件id
    :param suite: 测试套件参数
    :param user: 当前用户
    :return: 更新的测试套件信息
    """
    suite_obj=await TestSuites.get_or_none(id=suite_id)
    if not suite_obj:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    suites=await suite_obj.update_from_dict(suite.model_dump(exclude_unset=True))
    await suites.save()
    return SuiteParam(**suites.__dict__)

@test_router.delete("/suite/{suite_id}",description="删除测试套件",status_code=204)
async def delete_suite(suite_id:int):
    """
    删除测试套件
    :param suite_id: 测试套件id
    :param user: 当前用户
    :return: None
    """
    suite_obj=await TestSuites.get_or_none(id=suite_id)
    if not suite_obj:
        raise HTTPException(status_code=404, detail="测试套件不存在")
    await suite_obj.delete()
    return None

@test_router.post("/cases",response_model=CasesParam,description="添加测试用例")
async def add_cases(cases:AddCasesParam):
    """
    添加测试用例
    :param cases: 测试用例参数
    :param user: 当前用户
    :return: 添加的测试用例信息
    """
    project=await TestProject.get_or_none(id=cases.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    cases=await TestCases.create(name=cases.name,project_id=cases.project_id)
    return CasesParam(**cases.__dict__)
@test_router.get("/cases",response_model=list[CasesParam],description="获取测试用例列表")
async def get_cases(project_id:int|None=None):
    """
    获取测试用例列表
    :param project_id: 项目id
    :param user: 当前用户
    :return: 测试用例列表
    """
    que=TestCases.all()
    project=await TestProject.get_or_none(id=project_id)
    if project:
        que=que.filter(project_id=project_id)
    cases=await que.all()
    return [CasesParam(**case.__dict__) for case in cases]
@test_router.get("/cases/{cases_id}",response_model=CasesParam,description="获取测试用例详情")
async def get_cases_detail(cases_id:int):
    """
    获取测试用例详情
    :param cases_id: 测试用例id
    :param user: 当前用户
    :return: 测试用例详情
    """
    cases=await TestCases.get_or_none(id=cases_id)
    if not cases:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    return CasesParam(**cases.__dict__)

@test_router.put("/cases/{cases_id}",response_model=CasesParam,description="更新测试用例")
async def update_cases(cases_id:int,cases:UpdateCasesParam):
    """
    更新测试用例
    :param cases_id: 测试用例id
    :param cases: 测试用例参数
    :param user: 当前用户
    :return: 更新的测试用例信息
    """
    cases_obj=await TestCases.get_or_none(id=cases_id)
    if not cases_obj:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    cases=await cases_obj.update_from_dict(cases.model_dump(exclude_unset=True))
    await cases.save()
    return CasesParam(**cases.__dict__)
@test_router.delete("/cases/{cases_id}",description="删除测试用例",status_code=204)
async def delete_cases(cases_id:int):
    """
    删除测试用例
    :param cases_id: 测试用例id
    :param user: 当前用户
    :return: None
    """
    cases_obj=await TestCases.get_or_none(id=cases_id)
    if not cases_obj:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    await cases_obj.delete()

@test_router.post("/cases/{cases_id}",description="复制测试用例")
async def copy_cases(cases_id:int):
    """
    复制测试用例
    :param cases_id: 测试用例id
    :param user: 当前用户
    :return: None
    """
    cases_obj=await TestCases.get_or_none(id=cases_id)
    if not cases_obj:
        raise HTTPException(status_code=404, detail="测试用例不存在")
    cases=await TestCases.create(name=cases_obj.name,project_id=cases_obj.project_id,steps=cases_obj.steps)
    return CasesParam(**cases.__dict__)

@test_router.post("/suite/{suite_id}/cases",response_model=SuiteToCasesParam,description="套件中添加测试用例")
async def add_suite_cases(suite_id:int,item:AddSuiteToCasesParam):
    """
    套件中添加测试用例
    :param item: body 对象
    :param suite_id: 测试套件id
    :param user: 当前用户
    :return: 添加的测试用例信息
    """
    suite=await TestSuites.get_or_none(id=suite_id)
    cases=await TestCases.get_or_none(id=item.test_case_id)
    if not suite or not cases:
        raise HTTPException(status_code=404, detail="测试套件或测试用例不存在")
    suite_to_cases=await SuiteToCase.create(test_suite_id=suite_id,test_case_id=item.test_case_id,sort=item.sort)
    print(suite_to_cases.__dict__)
    return SuiteToCasesParam(**suite_to_cases.__dict__)

@test_router.delete("/suite/{suite_id}/cases/{id}",description="套件中删除测试用例",status_code=204)
async def delete_suite_cases(suite_id:int,id:int):
    """
    套件中删除测试用例
    :param id: 测试用例id
    :param user: 当前用户
    :return: None
    """
    suite_to_cases=await SuiteToCase.get_or_none(id=id,test_suite_id=suite_id)
    if not suite_to_cases:
        raise HTTPException(status_code=404, detail="测试用例不存在套件中")
    await suite_to_cases.delete()
    return None

@test_router.get("/suite/{suite_id}/cases",response_model=list[SuiteToCasesListParam],description="获取套件中的测试用例列表")
async def get_suite_cases(suite_id:int):
    """
    获取套件中的测试用例列表
    :param suite_id: 测试套件id
    :param user: 当前用户
    :return: 套件中的测试用例列表
    """
    que=SuiteToCase.all()
    que=que.filter(test_suite_id=suite_id).prefetch_related("test_case","test_suite").order_by("sort")
    suite_to_cases=await que.all()
    result=[]
    for suite_to_cases in suite_to_cases:
        item={
            "id": suite_to_cases.id,
            "test_case_id": suite_to_cases.test_case_id,
            "test_suite_id":suite_to_cases.test_suite_id,
            "sort": suite_to_cases.sort,
            "skip": suite_to_cases.skip,
            "test_suite_name": suite_to_cases.test_suite.name,
            "test_case_name": suite_to_cases.test_case.name
        }
        result.append(item)
    return result

@test_router.put("/suite/{suite_id}/cases/{id}",response_model=SuiteToCasesParam,description="更新套件中的测试用例状态")
async def update_suite_cases(suite_id:int,id:int):
    """
    更新套件中的测试用例状态
    :param suite_id: 测试套件id
    :param id: 测试用例id
    :param user: 当前用户
    :return: 更新的测试用例信息
    """
    suite_to_cases=await SuiteToCase.get_or_none(test_suite_id=suite_id,id=id)
    if not suite_to_cases:
        raise HTTPException(status_code=404, detail="测试用例不存在套件中")
    suite_to_cases.skip=not suite_to_cases.skip
    await suite_to_cases.save()
    return SuiteToCasesParam(**suite_to_cases.__dict__)


@test_router.put("/suite/{suite_id}/sort_case",description="更新套件中的测试用例排序")
async def update_suite_cases_sort(suite_id:int,items:list[UpdateSuiteToCasesParam]):
    """
    更新套件中的测试用例排序
    :param items:
    :param suite_id: 测试套件id
    :param user: 当前用户
    :return: None
    """
    obj=[]
    for item in items:
        suite_to_cases_=await SuiteToCase.get_or_none(id=item.id,test_suite_id=suite_id)
        if not suite_to_cases_:
            raise HTTPException(status_code=404, detail=f"测试用例不存在套件中用例ID：{item.id}")
        suite_to_cases_.sort=item.sort
        obj.append(suite_to_cases_)
    for i in obj:
        await i.save()
    return await SuiteToCase.filter(test_suite_id=suite_id).order_by("sort")