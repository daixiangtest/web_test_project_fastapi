"""
数据库的模型类
"""
from secrets import choice

from tortoise import models,fields

class TaskRecords(models.Model):
    """
    任务运行记录
    """
    id = fields.IntField(pk=True, description="任务运行记录id")
    project=fields.ForeignKeyField("models.TestProject",related_name="project",description="关联项目id")
    task=fields.ForeignKeyField("models.TestTasks",related_name="task",description="关联任务id")
    env=fields.JSONField(default={},description="运行环境")
    start_time=fields.DatetimeField(auto_now_add=True,description="开始时间")
    status=fields.CharField(max_length=20,default="INIT",description="运行状态",choice=[("INIT","待运行"),("RUNNING","运行中"),("FINISH","运行完成")])
    all=fields.IntField(default=0,description="运行总用例数")
    success=fields.IntField(default=0,description="运行成功用例数")
    run_all=fields.IntField(default=0,description="运行总次数")
    fail=fields.IntField(default=0,description="运行失败用例数")
    error=fields.IntField(default=0,description="运行错误用例数")
    skip=fields.IntField(default=0,description="运行跳过用例数")
    no_run=fields.IntField(default=0,description="未运行用例数")

    class Meta:
        table="task_records"
        indexes = [
            models.Index(fields=["project_id", "task_id"])
        ]
        description="任务运行记录表"
    def __str__(self):
        return self.task.name

class SuiteRecords(models.Model):
    """
    套件运行记录
    """
    id = fields.IntField(pk=True, description="套件运行记录id")
    suite=fields.ForeignKeyField("models.TestSuites",related_name="suite",description="关联套件id")
    task_record=fields.ForeignKeyField("models.TaskRecords",related_name="task_records",description="关联任务运行记录id",null=True,blank= True)
    status=fields.CharField(max_length=20,default="INIT",description="运行状态",choice=[("INIT","待运行"),("RUNNING","运行中"),("FINISH","运行完成")])
    all=fields.IntField(default=0,description="运行总用例数")
    success=fields.IntField(default=0,description="运行成功用例数")
    fail=fields.IntField(default=0,description="运行失败用例数")
    error=fields.IntField(default=0,description="运行错误用例数")
    skip=fields.IntField(default=0,description="运行跳过用例数")
    no_run=fields.IntField(default=0,description="未运行用例数")
    duration=fields.FloatField(default=0,description="运行时间")
    suite_log=fields.JSONField(default=[],description="运行日志")
    pass_rate=fields.FloatField(default=0,description="通过率")
    env=fields.JSONField(default={},description="运行环境",null=True,blank=True)
    class Meta:
        table="suite_records"
        description="套件运行记录表"

    def __str__(self):
        return self.suite.name

class CaseRecords(models.Model):
    """
    用例运行记录
    """
    id = fields.IntField(pk=True, description="用例运行记录id")
    case=fields.ForeignKeyField("models.TestCases",related_name="case",description="关联用例id")
    suite_record=fields.ForeignKeyField("models.SuiteRecords",related_name="suite_record",description="关联套件运行记录id",null=True,blank= True)
    run_info=fields.JSONField(default={},description="运行信息")
    status=fields.CharField(max_length=20,default="SUCCESS",description="运行状态",choice=[("SUCCESS","运行成功"),("FAIL","运行失败"),("ERROR","运行错误"),("SKIP","运行跳过"),("RUNNING","运行中")])

    class Meta:
        table="case_records"
        description="用例运行记录表"
    def __str__(self):
        return self.case.name