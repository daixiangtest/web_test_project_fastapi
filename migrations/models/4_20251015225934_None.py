from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用户id',
    `username` VARCHAR(32) NOT NULL COMMENT '用户名',
    `password` VARCHAR(128) NOT NULL COMMENT '密码',
    `nickname` VARCHAR(32) NOT NULL COMMENT '用户昵称',
    `mobile` VARCHAR(11) NOT NULL COMMENT '手机号' DEFAULT '',
    `email` VARCHAR(128) NOT NULL COMMENT '邮箱' DEFAULT '',
    `is_superuser` BOOL NOT NULL COMMENT '是否是员工' DEFAULT 0,
    `is_active` BOOL NOT NULL COMMENT '是否激活' DEFAULT 1
) CHARACTER SET utf8mb4 COMMENT='用户表';
CREATE TABLE IF NOT EXISTS `test_project` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '项目ID',
    `name` VARCHAR(50) NOT NULL COMMENT '项目名称',
    `crete_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `user_info_id` INT NOT NULL COMMENT '项目负责人',
    CONSTRAINT `fk_test_pro_users_4c4ff309` FOREIGN KEY (`user_info_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试项目表';
CREATE TABLE IF NOT EXISTS `project_module` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '项目模块ID',
    `name` VARCHAR(50) NOT NULL COMMENT '项目模块名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '项目模块创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `project_id` INT NOT NULL COMMENT '项目模块所属项目',
    CONSTRAINT `fk_project__test_pro_6a25756e` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='项目模块表';
CREATE TABLE IF NOT EXISTS `test_env` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '测试环境ID',
    `name` VARCHAR(50) NOT NULL COMMENT '测试环境名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '测试环境创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `host` VARCHAR(100) NOT NULL COMMENT '测试环境地址',
    `global_vars` JSON NOT NULL COMMENT '全局变量',
    `project_id` INT NOT NULL COMMENT '测试环境所属项目',
    CONSTRAINT `fk_test_env_test_pro_f21b8019` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试环境表';
CREATE TABLE IF NOT EXISTS `test_cases` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用例id',
    `name` VARCHAR(100) NOT NULL COMMENT '用例名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `steps` JSON COMMENT '用例步骤',
    `project_id` INT NOT NULL COMMENT '项目id',
    CONSTRAINT `fk_test_cas_test_pro_16b6e59b` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试用例表';
CREATE TABLE IF NOT EXISTS `test_suites` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '套件id',
    `name` VARCHAR(100) NOT NULL COMMENT '套件名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `suite_setup_step` JSON NOT NULL COMMENT '套件前置步骤',
    `suite_type` VARCHAR(50) NOT NULL COMMENT '套件类型' DEFAULT '功能',
    `modules_id` INT COMMENT '模块id',
    `project_id` INT NOT NULL COMMENT '项目id',
    CONSTRAINT `fk_test_sui_project__084e6d65` FOREIGN KEY (`modules_id`) REFERENCES `project_module` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_test_sui_test_pro_9423c086` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试套件表';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
