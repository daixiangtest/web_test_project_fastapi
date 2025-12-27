"""接口函数定义"""
import datetime

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import APIRouter, HTTPException, Depends
from tortoise import transactions

from apps.cases.models import TestSuites
from apps.corn.models import CornJob
from apps.corn.parameter import CornParam, CornUpdateParam
from apps.projects.models import TestProject, TestEnv
from apps.runner.models import TaskRecords, SuiteRecords, CaseRecords
from apps.tasks.models import TestTasks
from apps.users.models import Users
from comms.MQ_producer import MQProducer
from comms.auth import is_authenticated
import time
from comms.settings import REDIS_CONFIG
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import pytz

# 定时任务运行方法
async def run_task(corn_id,env_id, task_id):
    print(f"任务：{corn_id}", env_id, task_id)
    try:
        env=await TestEnv.get_or_none(id=env_id)
        task=await TestTasks.get_or_none(id=task_id).prefetch_related("suites","project")
        if not env or not task:
            print(f"Environment or task not found: env_id={env_id}, task_id={task_id}")
            return
        env_config = {
            "is_debug": False,
            "browser_type": "chromium",
            "host": env.host,
            "global_vars": env.global_vars
        }
        recode_task = await TaskRecords.create(
            project=task.project,
            task=task,
            status="RUNNING",
            env=env_config
        )
        task_count = 0
        for i in await task.suites.all():
            suite = await TestSuites.get_or_none(id=i.id).prefetch_related("suite_to_case")
            recode_suite = await SuiteRecords.create(
                suite=suite,
                status="RUNNING",
                env=env_config,
                task_record=recode_task
            )
            cases = []
            for j in await suite.suite_to_case.all():
                case = await j.test_case
                recode_case = await CaseRecords.create(
                    case=case,
                    status="RUNNING",
                    suite_record=recode_suite
                )
                cases.append({
                    "recode_case_id": recode_case.id,
                    "id": case.id,
                    "title": case.name,
                    "skip": j.skip,
                    "steps": case.steps}
                )
            recode_suite.all = len(cases)
            await recode_suite.save()
            test_case = {
                "recode_task_id": recode_task.id,
                "recode_suite_id": recode_suite.id,
                "id": suite.id,
                "name": suite.name,
                # 前置操作
                "setup_step": suite.suite_setup_step,
                # 用例集
                "cases": cases
            }
            task_count += len(cases)
            print(test_case, env_config)
            MQProducer().send_test_task(env_config, test_case)
        recode_task.all = task_count
        await recode_task.save()
        print(f"任务{corn_id}已经提交执行")
    except Exception as e:
        print(f"任务{corn_id}执行失败: {str(e)}")


# 定时任务配置=======================================================
# 指定本地时间
local_time=pytz.timezone('Asia/Shanghai')
# 创建任务器的配置
jonstore={
    'default':RedisJobStore(**REDIS_CONFIG)
}
# 任务执行器
executors={
    'default':ThreadPoolExecutor(max_workers=10)
}
job_defults={
    'coalesce':False,
    'max_instances':10
}
# 创建调度器(同步调度)
# scheduler = BackgroundScheduler(job_defults=job_defults, jobstores=jonstore, executors=executors, timezone=local_time)
# 创建异步任务调度器
scheduler=AsyncIOScheduler(job_defults=job_defults, jobstores=jonstore, timezone=local_time)
# 启动调度器
scheduler.start()
# 定时任务配置=======================================================

cron_router=APIRouter(prefix="/api/cron",tags=["定时任务管理"],dependencies=[Depends(is_authenticated)])

@cron_router.post("/crontab")
async def create_job(param:CornParam):
    """
    创建定时任务
    :param param:
    :return:
    """
    # 创建任务id
    cron_task_id=str(int(time.time()))
    print("参数",param)
    # 校验参数是否正确
    project=await TestProject.get_or_none(id=param.project_id)
    if not project:
        raise HTTPException(status_code=404,detail="项目不存在")
    task=await TestTasks.get_or_none(id=param.task_id).prefetch_related("suites","project")
    if not task:
        raise HTTPException(status_code=404,detail="任务不存在")
    env=await TestEnv.get_or_none(id=param.env_id)
    if not env:
        raise HTTPException(status_code=404, detail="环境不存在")
    if param.run_type not in["interval","date","crontab"]:
        raise HTTPException(status_code=404,detail="任务类型错误")
    if param.date is not None and param.date<=datetime.datetime.now() and param.run_type=="date":
        raise HTTPException(status_code=404,detail="时间错误")
    async with transactions.in_transaction() as cron_task:
        try:
            # 创建任务
            if param.run_type=="interval":
                param.date=None
                param.crontab=None
                trigger=IntervalTrigger(seconds=param.interval,timezone=local_time)
            elif param.run_type=="date":
                param.interval=None
                param.crontab=None
                trigger=DateTrigger(run_date=param.date, timezone=local_time)
            else:
                param.interval=None
                param.date=None
                trigger = CronTrigger(**param.crontab.model_dump(), timezone=local_time)
            # 添加任务
            print(f"env type: {type(env)}, env.id type: {type(env.id)}")
            print(f"env.id value: {env.id}")
            scheduler.add_job(func=run_task, trigger=trigger, id=cron_task_id, args=[cron_task_id,env.id, task.id])
            # 定时任务记录
            res=await CornJob.create(id=cron_task_id,
                                 name=param.name,
                                 project=project,
                                 env=env,
                                 task=task,
                                 state=True,
                                 run_type=param.run_type,
                                 interval=param.interval,
                                 date=param.date,
                                 crontab=param.crontab)
        except Exception as e:
            await cron_task.rollback()
            scheduler.remove_job(cron_task_id)
            raise e
            # raise HTTPException(status_code=405,detail=str(f"添加定时任务失败，失败原因为：{e}"))
        else:
            await cron_task.commit()
            return res


@cron_router.get("/crontab")
async def get_jobs(project_id:int):
    """
    获取定时任务列表
    :return:
    """
    res=await CornJob.filter(project_id=project_id).all()
    return res

@cron_router.delete("/crontab/{id}",status_code=204)
async def delete_job(id:str):
    """
    删除定时任务
    :param id:
    :return:
    """
    async with transactions.in_transaction() as delete_job:
        try:
            job=await CornJob.get_or_none(id=id)
            if not job:
                raise HTTPException(status_code=404,detail="定时任务不存在")
            scheduler.remove_job(id)
            await job.delete()
        except Exception as e:
            await delete_job.rollback()
            raise HTTPException(status_code=405,detail=str(f"删除定时任务失败，失败原因为：{e}"))

@cron_router.patch("/crontab/{id}")
async def update_state_job(id:str):
    """
    更新定时任务状态
    :param id:
    :return:
    """
    job=await CornJob.get_or_none(id=id)
    if not job:
        raise HTTPException(status_code=404,detail="定时任务不存在")
    async with transactions.in_transaction() as update_job:
        try:
            if job.state:
                job.state=False
                await job.save()
                scheduler.pause_job(id)
            else:
                job.state=True
                await job.save()
                scheduler.resume_job(id)
            return job
        except Exception as e:
            await update_job.rollback()
            raise HTTPException(status_code=405,detail=str(f"更新定时任务失败，失败原因为：{e}"))


@cron_router.put("/crontab/{id}")
async def update_config_job(id:str,param:CornUpdateParam):
    """
    更新定时任务配置
    :param id:
    :param param:
    :return:
    """
    task_job=await CornJob.get_or_none(id=id)
    if not task_job:
        raise HTTPException(status_code=404,detail="定时任务不存在")
    if param.run_type not in["interval","date","crontab"]:
        raise HTTPException(status_code=404,detail="任务类型错误")
    if param.date is not None and param.date<=datetime.datetime.now() and param.run_type=="date":
        raise HTTPException(status_code=404,detail="时间错误")
    try:
        # 创建任务
        if param.run_type=="interval":
            param.crontab=None
            trigger=IntervalTrigger(seconds=param.interval,timezone=local_time)
        elif param.run_type=="date":
            param.crontab=None
            trigger=DateTrigger(run_date=param.date, timezone=local_time)
        else:
            param.date=None
            trigger = CronTrigger(**param.crontab.model_dump(), timezone=local_time)
        # 更改任务
        scheduler.modify_job(job_id=id, trigger=trigger)
        # 更改定时任务记录
        update_data = param.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task_job, field):
                setattr(task_job, field, value)
        await task_job.save()
        return task_job
    except Exception as e:
        raise e
        # raise HTTPException(status_code=405,detail=str(f"更改定时任务类型失败，失败原因为：{e}")
