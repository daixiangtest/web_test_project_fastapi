"""
数据库的模型类
"""


from tortoise import models,fields

class TestCases(models.Model):
    """
    测试用例表
    """
    id = fields.IntField(pk=True, description="用例id")
    name = fields.CharField(max_length=100, description="用例名称")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    project = fields.ForeignKeyField("models.TestProject", related_name="test_cases", description="项目id")
    steps=fields.JSONField(description="用例步骤",default=list,null=True)
    class Meta:
        table="test_cases"
        table_description="测试用例表"

class TestSuites(models.Model):
    """
    测试套件表
    """
    id=fields.IntField(pk=True, description="套件id")
    name = fields.CharField(max_length=100, description="套件名称")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    project = fields.ForeignKeyField("models.TestProject", related_name="test_suites", description="项目id")
    modules = fields.ForeignKeyField("models.ProjectModule", related_name="test_suites", description="模块id", null=True,Blank= True)
    suite_setup_step = fields.JSONField(description="套件前置步骤",default=list)
    # 套件类型 choices 规定字段的可选值和对应的枚举映射
    suite_type=fields.CharField(max_length=50,description="套件类型",choices=[(1,"功能"),(2,"业务流")],default="功能")
    class Meta:
        table="test_suites"
        table_description="测试套件表"



class SuiteToCase(models.Model):
    """
    测试套件和测试用例关系表
    """
    id = fields.IntField(pk=True, description="关系id")
    test_suite = fields.ForeignKeyField("models.TestSuites", related_name="suite_to_case", description="测试套件id")
    test_case = fields.ForeignKeyField("models.TestCases", related_name="suite_to_case", description="测试用例id")
    sort=fields.IntField(description="用例顺序",default=0)
    skip = fields.BooleanField(description="是否跳过", default=False, null=True)
    class Meta:
        table="suite_to_case"
        table_description="测试套件和测试用例关系表"