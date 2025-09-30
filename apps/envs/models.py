"""
数据库的模型类
"""

from tortoise import models,fields

class Envs(models.Model):
    """
    环境表
    """
    id=fields.IntField(pk=True, description="环境id")
    name = fields.CharField(max_length=100, unique=True, description="环境名称")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    project = fields.ForeignKeyField("models.Projects", related_name="envs", description="项目id")
    host=fields.CharField(max_length=200, description="环境地址")
    global_vars=fields.JSONField(description="全局变量",default=dict)