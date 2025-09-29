"""
数据库的模型类
"""

from tortoise import fields,Model

class Users(Model):
    """
    用户模型类
    """
    id = fields.IntField(pk=True, description="用户id")
    username = fields.CharField(max_length=32,description="用户名")
    password = fields.CharField(max_length=128,description="密码")
    nickname = fields.CharField(max_length=32,description="用户昵称")
    mobile = fields.CharField(max_length=11,description="手机号",default="")
    email = fields.CharField(max_length=128,description="邮箱",default="")
    is_superuser = fields.BooleanField(default=False,description="是否是员工")
    is_active = fields.BooleanField(default=True,description="是否激活")

    def __str__(self):
        return self.username

    class Meta:
        table = "users"
        table_description = "用户表"