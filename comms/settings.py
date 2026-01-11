"""
项目的全局配置文件
"""

# 数据库连接配置
# db_config = {
#     "host": "115.120.244.181",
#     "port": 3306,
#     "user": "root",
#     "password": "Dx3826729123",
#     "database": "web_config",
# }
db_config = {
    "host": "127.0.0.1",
    # "host":"9706ih4dm038.vicp.fun",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "web_config",
}


# 数据库模型
db_models = [
    "apps.users.models",
    "apps.projects.models",
    "apps.cases.models",
    "apps.tasks.models",
    "apps.runner.models",
    "apps.corn.models"
]
# 数据库连接
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": db_config
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models", *db_models],
            "default_connection": "default",
        }
    }
}

# jwt token秘钥
SECRET_KEY="fed1db48d2c825f964b2a15ed17410c3754a519df5c053de964fd75ed14c4a25"
# jwt token有效期
ACCESS_TOKEN_EXPIRE_MINUTES=3600*24

# RabbitMQ配置
MQ_CONFIG = {
    "host": "localhost",
    "port": 5672,
    "queue_name": "test_web",
}

REDIS_CONFIG={
    "host": "localhost",
    "port": 6379,
    "db": 1
}