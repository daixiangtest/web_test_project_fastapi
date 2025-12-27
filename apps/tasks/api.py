"""接口函数定义"""
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from apps.cases.models import TestSuites
from apps.projects.models import TestProject
from apps.tasks.models import TestTasks
from apps.tasks.parameter import AddTaskParam, TaskParam, UpdateTaskParam, TaskDetailParam, TaskSuiteParam
from comms.auth import is_authenticated

task_router=APIRouter(prefix="/api/plan",tags=["任务管理"],dependencies=[Depends(is_authenticated)])


@task_router.post("/task",response_model=TaskParam,description="添加测试任务")
async def add_task(task:AddTaskParam):
    """
    添加测试任务
    """
    project_obj=await TestProject.get(id=task.project_id)
    if not project_obj:
        raise HTTPException(status_code=400,detail="项目不存在")
    task_obj=await TestTasks.create(**task.model_dump())
    return TaskParam(**task_obj.__dict__)

@task_router.get("/task",response_model=List[TaskParam],description="获取测试任务列表")
async def get_task(project_id:int):
    """
    获取测试任务
    """
    task_objs=await TestTasks.filter(project=project_id)
    return [TaskParam(**task_obj.__dict__) for task_obj in task_objs]

@task_router.delete("/task",status_code=204)
async def delete_task(task_id:int):
    """
    删除测试任务
    """
    task_obj=await TestTasks.get_or_none(id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404,detail="任务不存在")
    await task_obj.delete()

@task_router.put("/task",response_model=TaskParam,description="更新测试任务名称")
async def update_task(task_id:int,task:UpdateTaskParam):
    """
    更新测试任务名称
    """
    task_obj=await TestTasks.get_or_none(id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404,detail="任务不存在")
    task_obj.name=task.name
    await task_obj.save()
    return TaskParam(**task_obj.__dict__)

@task_router.post("/task/{task_id}/suite",response_model=TaskDetailParam,description="添加测试套件到用例中")
async def add_suite_to_task(task_id:int,suite_id:int):
    """
    添加测试套件到用例中
    """
    task_obj=await TestTasks.get_or_none(id=task_id,)
    if not task_obj:
        raise HTTPException(status_code=404,detail="任务不存在")
    suite_obj=await TestSuites.get_or_none(id=suite_id)
    if not suite_obj:
        raise HTTPException(status_code=404,detail="测试套件不存在")
    await task_obj.suites.add(suite_obj)

    suite_data=[]
    for suite in await task_obj.suites:
        suite_data.append(TaskSuiteParam(**suite.__dict__))
    result=TaskDetailParam(
        suites=suite_data,
        id=task_obj.id,
        name=task_obj.name,
        project_id=task_obj.project_id,
        create_time=task_obj.create_time
         )
    return result

@task_router.delete("/task/{task_id}/suite",status_code=204,description="删除测试套件中的用例")
async def delete_suite_to_task(task_id:int,suite_id:int):
    """
    删除测试套件中的用例
    """
    task_obj=await TestTasks.get_or_none(id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404,detail="任务不存在")
    suite_obj=await TestSuites.get_or_none(id=suite_id)
    if not suite_obj:
        raise HTTPException(status_code=404,detail="测试套件不存在")
    await task_obj.suites.remove(suite_obj)


@task_router.get("/task/{task_id}",response_model=TaskDetailParam,description="获取测试任务详情")
async def get_task_detail(task_id: int):
    """
    获取测试任务详情
    """
    task_obj=await TestTasks.get_or_none(id=task_id)
    if not task_obj:
        raise HTTPException(status_code=404,detail="任务不存在")
    suite_data=[]
    for suite in await task_obj.suites:
        suite_data.append(TaskSuiteParam(**suite.__dict__))
    result=TaskDetailParam(
        suites=suite_data,
        id=task_obj.id,
        name=task_obj.name,
        project_id=task_obj.project_id,
        create_time=task_obj.create_time
    )
    return result
