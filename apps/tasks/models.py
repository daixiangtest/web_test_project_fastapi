"""
数据库的模型类
"""
from email.policy import default

from tortoise import models,fields

class TestTasks(models.Model):
    """
    测试任务
    """
    id=fields.IntField(pk=True,description="任务id")
    name=fields.CharField(max_length=100,description="任务名称")
    create_time=fields.DatetimeField(auto_now_add=True,description="创建时间")
    project=fields.ForeignKeyField("models.TestProject",related_name="test_project",description="项目id")
    suites=fields.ManyToManyField("models.TestSuites",related_name="test_suite",description="任务用例套件",null=True,default= list,blank=True)

    class  Meta:
        table="test_tasks"
        table_description="测试任务"

    def __str__(self):
        return self.name

