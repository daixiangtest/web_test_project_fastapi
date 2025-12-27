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
) CHARACTER SET utf8mb4 COMMENT='测试套件表';
CREATE TABLE IF NOT EXISTS `suite_to_case` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '关系id',
    `sort` INT NOT NULL COMMENT '用例顺序' DEFAULT 0,
    `skip` BOOL COMMENT '是否跳过' DEFAULT 0,
    `test_case_id` INT NOT NULL COMMENT '测试用例id',
    `test_suite_id` INT NOT NULL COMMENT '测试套件id',
    CONSTRAINT `fk_suite_to_test_cas_2356db16` FOREIGN KEY (`test_case_id`) REFERENCES `test_cases` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_suite_to_test_sui_5c52fd61` FOREIGN KEY (`test_suite_id`) REFERENCES `test_suites` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试套件和测试用例关系表';
CREATE TABLE IF NOT EXISTS `test_tasks` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '任务id',
    `name` VARCHAR(100) NOT NULL COMMENT '任务名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '创建时间' DEFAULT CURRENT_TIMESTAMP(6),
    `project_id` INT NOT NULL COMMENT '项目id',
    CONSTRAINT `fk_test_tas_test_pro_ea4f9b01` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='测试任务';
CREATE TABLE IF NOT EXISTS `task_records` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '任务运行记录id',
    `env` JSON NOT NULL COMMENT '运行环境',
    `start_time` DATETIME(6) NOT NULL COMMENT '开始时间' DEFAULT CURRENT_TIMESTAMP(6),
    `status` VARCHAR(20) NOT NULL COMMENT '运行状态' DEFAULT 'INIT',
    `all` INT NOT NULL COMMENT '运行总用例数' DEFAULT 0,
    `success` INT NOT NULL COMMENT '运行成功用例数' DEFAULT 0,
    `run_all` INT NOT NULL COMMENT '运行总次数' DEFAULT 0,
    `fail` INT NOT NULL COMMENT '运行失败用例数' DEFAULT 0,
    `error` INT NOT NULL COMMENT '运行错误用例数' DEFAULT 0,
    `skip` INT NOT NULL COMMENT '运行跳过用例数' DEFAULT 0,
    `no_run` INT NOT NULL COMMENT '未运行用例数' DEFAULT 0,
    `project_id` INT NOT NULL COMMENT '关联项目id',
    `task_id` INT NOT NULL COMMENT '关联任务id',
    CONSTRAINT `fk_task_rec_test_pro_8f0d96ec` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_task_rec_test_tas_a3ba2412` FOREIGN KEY (`task_id`) REFERENCES `test_tasks` (`id`) ON DELETE CASCADE,
    KEY `idx_task_record_project_5de4e4` (`project_id`, `task_id`)
) CHARACTER SET utf8mb4 COMMENT='任务运行记录';
CREATE TABLE IF NOT EXISTS `suite_records` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '套件运行记录id',
    `status` VARCHAR(20) NOT NULL COMMENT '运行状态' DEFAULT 'INIT',
    `all` INT NOT NULL COMMENT '运行总用例数' DEFAULT 0,
    `success` INT NOT NULL COMMENT '运行成功用例数' DEFAULT 0,
    `fail` INT NOT NULL COMMENT '运行失败用例数' DEFAULT 0,
    `error` INT NOT NULL COMMENT '运行错误用例数' DEFAULT 0,
    `skip` INT NOT NULL COMMENT '运行跳过用例数' DEFAULT 0,
    `no_run` INT NOT NULL COMMENT '未运行用例数' DEFAULT 0,
    `duration` DOUBLE NOT NULL COMMENT '运行时间' DEFAULT 0,
    `suite_log` JSON NOT NULL COMMENT '运行日志',
    `pass_rate` DOUBLE NOT NULL COMMENT '通过率' DEFAULT 0,
    `env` JSON COMMENT '运行环境',
    `suite_id` INT NOT NULL COMMENT '关联套件id',
    `task_record_id` INT COMMENT '关联任务运行记录id',
    CONSTRAINT `fk_suite_re_test_sui_dec3410b` FOREIGN KEY (`suite_id`) REFERENCES `test_suites` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_suite_re_task_rec_45c2923b` FOREIGN KEY (`task_record_id`) REFERENCES `task_records` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='套件运行记录';
CREATE TABLE IF NOT EXISTS `case_records` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '用例运行记录id',
    `run_info` JSON NOT NULL COMMENT '运行信息',
    `status` VARCHAR(20) NOT NULL COMMENT '运行状态' DEFAULT 'SUCCESS',
    `case_id` INT NOT NULL COMMENT '关联用例id',
    `suite_record_id` INT COMMENT '关联套件运行记录id',
    CONSTRAINT `fk_case_rec_test_cas_e19eddfc` FOREIGN KEY (`case_id`) REFERENCES `test_cases` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_case_rec_suite_re_fa218702` FOREIGN KEY (`suite_record_id`) REFERENCES `suite_records` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用例运行记录';
CREATE TABLE IF NOT EXISTS `crontab` (
    `id` VARCHAR(100) NOT NULL PRIMARY KEY COMMENT '任务id',
    `name` VARCHAR(50) NOT NULL COMMENT '任务名称',
    `create_time` DATETIME(6) NOT NULL COMMENT '创建日期' DEFAULT CURRENT_TIMESTAMP(6),
    `state` BOOL NOT NULL COMMENT '是否启用' DEFAULT 1,
    `run_type` VARCHAR(10) NOT NULL COMMENT '任务类型',
    `interval` INT COMMENT '执行间隔时间' DEFAULT 60,
    `date` DATETIME(6) COMMENT '指定执行的事件' DEFAULT '2030-01-01 00:00:00',
    `crontab` JSON COMMENT '周期性任务规则',
    `env_id` INT NOT NULL COMMENT '执行环境',
    `project_id` INT NOT NULL COMMENT '所属项目',
    `task_id` INT NOT NULL COMMENT '执行的测试任务',
    CONSTRAINT `fk_crontab_test_env_1f2df3c6` FOREIGN KEY (`env_id`) REFERENCES `test_env` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_crontab_test_pro_1e6b4863` FOREIGN KEY (`project_id`) REFERENCES `test_project` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_crontab_test_tas_518adae3` FOREIGN KEY (`task_id`) REFERENCES `test_tasks` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='定时任务表';
CREATE TABLE IF NOT EXISTS `test_tasks_test_suites` (
    `test_tasks_id` INT NOT NULL,
    `testsuites_id` INT NOT NULL,
    FOREIGN KEY (`test_tasks_id`) REFERENCES `test_tasks` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`testsuites_id`) REFERENCES `test_suites` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_test_tasks__test_ta_f8524e` (`test_tasks_id`, `testsuites_id`)
) CHARACTER SET utf8mb4 COMMENT='任务用例套件';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
