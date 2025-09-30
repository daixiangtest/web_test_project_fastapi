"""
数据库的模型类
"""

from tortoise import models,fields

class TestProject(models.Model):
    """
    测试项目表
    """
    id=fields.IntField(pk=True, description="项目ID")
    name=fields.CharField(max_length=50,description="项目名称")
    crete_time=fields.DatetimeField(auto_now_add=True,description="创建时间")
    user_info=fields.ForeignKeyField("models.Users",related_name="projects",description="项目负责人")

    def __str__(self):
        return self.name
    class Meta:
        table="test_project"
        table_description="测试项目表"

class TestEnv(models.Model):
    """
    测试环境表
    """
    id=fields.IntField(pk=True, description="测试环境ID")
    name=fields.CharField(max_length=50,description="测试环境名称")
    create_time=fields.DatetimeField(auto_now_add=True,description="测试环境创建时间")
    project=fields.ForeignKeyField("models.TestProject",related_name="envs",description="测试环境所属项目")
    host=fields.CharField(max_length=100,description="测试环境地址")
    global_vars=fields.JSONField(description="全局变量",default=dict)
    def __str__(self):
        return self.name
    class Meta:
        table="test_env"
        table_description="测试环境表"

class ProjectModule(models.Model):
    """
    项目模块表
    """
    id=fields.IntField(pk=True, description="项目模块ID")
    name=fields.CharField(max_length=50,description="项目模块名称")
    project=fields.ForeignKeyField("models.TestProject",related_name="modules",description="项目模块所属项目")
    create_time=fields.DatetimeField(auto_now_add=True,description="项目模块创建时间")

    def __str__(self):
        return self.name
    class Meta:
        table="project_module"
        table_description="项目模块表"