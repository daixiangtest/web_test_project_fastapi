from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `test_env` MODIFY COLUMN `global_vars` JSON NOT NULL COMMENT '全局变量';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `test_env` MODIFY COLUMN `global_vars` LONGTEXT NOT NULL COMMENT '全局变量';"""
