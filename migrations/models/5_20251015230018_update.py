from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `suite_to_case` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '关系id',
    `sort` INT NOT NULL COMMENT '用例顺序' DEFAULT 0,
    `skip` BOOL COMMENT '是否跳过' DEFAULT 0,
    `test_case_id` INT NOT NULL COMMENT '测试用例id',
    `test_suite_id` INT NOT NULL COMMENT '测试套件id',
    CONSTRAINT `fk_suite_to_test_cas_2356db16` FOREIGN KEY (`test_case_id`) REFERENCES `test_cases` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_suite_to_test_sui_5c52fd61` FOREIGN KEY (`test_suite_id`) REFERENCES `test_suites` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试套件和测试用例关系表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `suite_to_case`;"""
