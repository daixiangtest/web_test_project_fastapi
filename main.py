import uvicorn
from fastapi import FastAPI
from starlette.config import Config
from tortoise.contrib.fastapi import register_tortoise

from apps.users.api import user_router
from apps.projects.api import pro_router
from comms.settings import TORTOISE_ORM
app = FastAPI(
    title="FastAPI_web_project",
    description="web 自动化项目",
    version="0.1.0"
)

# 注册路由
app.include_router(user_router)
app.include_router(pro_router)

# 注册数据模型
register_tortoise(app, config=TORTOISE_ORM)

if __name__ == '__main__':
    """
        项目运行步骤
        首次迁移数据
            初始化模型生成迁移文件
            aerich init -t comms.settings.TORTOISE_ORM
            初始化数据库连接并创建表
            aerich init-db
        后续变更模型执行
            修改模型后执行生成新的迁移文件
            aerich migrate
            更改表结构
            aerich upgrade
        运行文件启动服务
        通过fastapi 终端运行

        """

    uvicorn.run(app, host="127.0.0.1", port=8000)