"""接口函数定义"""

from fastapi import APIRouter, HTTPException, Depends

from apps.tasks.models import TestTasks
from playwright_test.core.run import Runner
from apps.cases.models import TestCases,TestSuites
from apps.projects.models import TestEnv
from apps.runner.parameter import RunCaseParam,CaseResulParam,SuiteResulParam,TaskResulParam
from apps.runner.models import TaskRecords,SuiteRecords,CaseRecords
from comms.MQ_producer import MQProducer
from comms.auth import is_authenticated



run_router=APIRouter(prefix="/api/run",tags=["执行管理"],dependencies=[Depends(is_authenticated)])

@run_router.post("/cases/{id}",description="执行用例")
async def run_cases(id:int,item:RunCaseParam):
    """
    执行用例
    :param id: 用例id
    :param user: 用户
    :return:
    """
    # 获取case用例数据
    case=await TestCases.get_or_none(id=id)
    if not case:
        raise HTTPException(status_code=404, detail="用例不存在")
    # 获取环境信息
    env=await TestEnv.get_or_none(id=item.env_id)
    if not env:
        raise HTTPException(status_code=404, detail="环境不存在")
    if item.browser_type in ["chromium","firefox","webkit"]:
        browser_type=item.browser_type
    else:
        browser_type="chromium"
    # 创建用例执行记录
    recode_case=await CaseRecords.create(
        case=case,
        status="RUNNING"
    )
    env_config = {
        "is_debug": False,
        "browser_type": browser_type,
        "host": env.host,
        "global_vars":env.global_vars
    }

    test_case = {
        "id": "编号",
        "name": "调试用例",
        # 前置操作
        "setup_step": [
        ],
        # 用例集
        "cases": [
            {
                "recode_case_id":recode_case.id,
                "id": case.id,
                "title": case.name,
                "skip": False,
                "steps": case.steps}
        ]
    }
    print(test_case,env_config)
    # 提交任务到运行器中进行执行
    # res=Runner(env_config, test_case).run()
    MQProducer().send_test_task(env_config, test_case)
    return {"message":"测试任务提交成功"}


@run_router.post("/suite/{id}",description="执行用例集")
async def run_suite(id:int,item:RunCaseParam):
    """
    执行用例集
    :param id: 用例集id
    :param user: 用户
    :return:
    """
    suite=await TestSuites.get_or_none(id=id).prefetch_related("suite_to_case")
    if not suite:
        raise HTTPException(status_code=404, detail="用例集不存在")
    env=await TestEnv.get_or_none(id=item.env_id)
    if not env:
        raise HTTPException(status_code=404, detail="环境不存在")
    browser_type=item.browser_type if item.browser_type in ["chromium","firefox","webkit"] else "chromium"
    env_config = {
        "is_debug": False,
        "browser_type": browser_type,
        "host": env.host,
        "global_vars": env.global_vars
    }
    recode_suite = await SuiteRecords.create(
        suite=suite,
        status="RUNNING",
        env=env_config
    )

    cases=[]
    for i in await suite.suite_to_case.all():
        case=await i.test_case
        recode_case = await CaseRecords.create(
            case=case,
            suite_record=recode_suite,
            status="RUNNING"
        )
        cases.append({
            "recode_case_id":recode_case.id,
            "id": case.id,
            "title": case.name,
            "skip": i.skip,
            "steps": case.steps}
        )
    # 创建测试套件执行记录
    recode_suite.all=len(cases)
    await recode_suite.save()
    test_case = {
        "recode_suite_id":recode_suite.id,
        "id": suite.id,
        "name": suite.name,
        # 前置操作
        "setup_step": suite.suite_setup_step,
        # 用例集
        "cases": cases
    }
    print(test_case,env_config)
    MQProducer().send_test_task(env_config, test_case)
    return {"message": "测试套件提交成功"}

@run_router.post("/task/{id}",description="执行测试任务")
async def run_task(id:int,item:RunCaseParam):
    """
    执行测试任务
    :param item: 请求参数
    :param id: 任务id
    :return:
    """
    task=await TestTasks.get_or_none(id=id).prefetch_related("suites","project")
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    env=await TestEnv.get_or_none(id=item.env_id)
    if not env:
        raise HTTPException(status_code=404, detail="环境不存在")
    browser_type=item.browser_type if item.browser_type in ["chromium","firefox","webkit"] else "chromium"
    env_config = {
        "is_debug": False,
        "browser_type": browser_type,
        "host": env.host,
        "global_vars": env.global_vars
    }
    recode_task=await TaskRecords.create(
        project=task.project,
        task=task,
        status="RUNNING",
        env=env_config
    )
    task_count=0
    for i in await task.suites.all():
        suite=await TestSuites.get_or_none(id=i.id).prefetch_related("suite_to_case")
        recode_suite = await SuiteRecords.create(
            suite=suite,
            status="RUNNING",
            env=env_config,
            task_record=recode_task
        )
        cases=[]
        for j in await suite.suite_to_case.all():
            case = await j.test_case
            recode_case = await CaseRecords.create(
                case=case,
                status="RUNNING",
                suite_record=recode_suite
            )
            cases.append({
                "recode_case_id":recode_case.id,
                "id": case.id,
                "title": case.name,
                "skip": j.skip,
                "steps": case.steps}
            )
        recode_suite.all=len(cases)
        await recode_suite.save()
        test_case = {
            "recode_task_id":recode_task.id,
            "recode_suite_id":recode_suite.id,
            "id": suite.id,
            "name": suite.name,
            # 前置操作
            "setup_step": suite.suite_setup_step,
            # 用例集
            "cases": cases
        }
        task_count+=len(cases)
        print(test_case,env_config)
        MQProducer().send_test_task(env_config, test_case)
    recode_task.all=task_count
    await recode_task.save()
    return {"message": "测试任务提交成功"}


@run_router.get("/task/records",description="获取测试任务执行记录")
async def get_task_records(project_id:int,task_id:int|None=None,page:int=1,page_size:int=10):
    """
    获取测试任务执行记录
    :param page_size:
    :param page:
    :param task_id:
    :param project_id: 项目id
    :return:
    """
    task_records=TaskRecords.filter(project_id=project_id)
    if task_id:
        task_records=task_records.filter(task_id=task_id)
    task_records=task_records.order_by("-id")
    total=await task_records.count()
    data=await task_records.offset((page-1)*page_size).limit(page_size).prefetch_related("task")
    return {"total":total,"data":data}

@run_router.get("/suite/records",description="获取测试任务执行记录详情")
async def get_task_record(task_record_id:int= None,suite_id:int= None,page:int=1,page_size:int=10):
    """
    获取测试任务执行记录详情
    :param task_record_id:
    :param page_size:
    :param page:
    :param suite_id:
    :return:
    """
    suite_records=SuiteRecords.all()

    if suite_id:
        records_type="suite"
        suite_records=suite_records.filter(suite_id=suite_id)
    elif task_record_id:
        records_type="task_records"
        suite_records=suite_records.filter(task_record_id=task_record_id)
    else:
        raise HTTPException(status_code=404, detail="task_id 和 task_record_id 必须传入一个")
    total=await suite_records.count()
    data=await suite_records.offset((page-1)*page_size).limit(page_size).prefetch_related("suite")
    return {"records_type":records_type,"total":total,"data":data}

@run_router.get("/case/records",description="获取用例执行记录")
async def get_case_records(suite_record_id:int= None,case_id:int= None,page:int=1,page_size:int=10):
    """
    获取用例执行记录
    :param suite_record_id:
    :param case_id:
    :param page_size:
    :param page:
    :return:
    """
    case_records=CaseRecords.all()
    if case_id:
        case_records=case_records.filter(case_id=case_id)
        records_type="case"
    elif suite_record_id:
        case_records=case_records.filter(suite_record_id=suite_record_id)
        records_type="suite_records"
    else:
        raise HTTPException(status_code=404, detail="suite_record_id 和 case_id 必须传入一个")
    total=await case_records.count()
    data=await case_records.offset((page-1)*page_size).limit(page_size).prefetch_related("case")
    return {"records_type":records_type,"total":total,"data":data}

@run_router.get("/case/record/{id}",description="获取用例执行记录详情",response_model=CaseResulParam)
async def get_case_record(id:int):
    """
    获取用例执行记录详情
    :param id:
    :return:
    """
    case_record=await CaseRecords.get_or_none(id=id).prefetch_related("case")
    if not case_record:
        raise HTTPException(status_code=404, detail="用例执行记录不存在")
    return CaseResulParam(**case_record.__dict__,case_name=case_record.case.name)

@run_router.get("/suite/record/{id}",description="获取用例执行记录详情",response_model=SuiteResulParam)
async def get_suite_record(id:int):
    """
    获取用例执行记录详情
    :param id:
    :return:
    """
    suite_record=await SuiteRecords.get_or_none(id=id).prefetch_related("suite")
    if not suite_record:
        raise HTTPException(status_code=404, detail="用例执行记录不存在")
    return SuiteResulParam(**suite_record.__dict__,suite_name=suite_record.suite.name)

@run_router.get("/task/record/{id}",description="获取用例执行记录详情",response_model=TaskResulParam)
async def get_task_record(id:int):
    """
    获取用例执行记录详情
    :param id:
    :return:
    """
    task_record=await TaskRecords.get_or_none(id=id).prefetch_related("task")
    if not task_record:
        raise HTTPException(status_code=404, detail="用例执行记录不存在")
    return task_record
