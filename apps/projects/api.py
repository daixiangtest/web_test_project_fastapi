"""接口函数定义"""

from fastapi import APIRouter, HTTPException, Depends
from apps.projects.parameter import ProjectParam, ProjectResult, TestEnvParam, AddEnvParam, UpdateEnvParam
from apps.projects.models import TestProject, TestEnv
from apps.users.models import Users
from comms.auth import is_authenticated

pro_router = APIRouter(prefix="/api/pro", tags=["项目管理"])


@pro_router.post("/projects", response_model=ProjectResult, description="创建项目")
async def create_project(item: ProjectParam, user_info: Users = Depends(is_authenticated)):
    """创建项目"""
    project = await TestProject.create(name=item.name, user_info=user_info)
    return ProjectResult(**project.__dict__)


@pro_router.get("/projects", response_model=list[ProjectResult], description="获取项目列表")
async def get_projects(user_info: Users = Depends(is_authenticated)):
    """获取项目列表"""
    # 通过用户id项目列表
    projects = await TestProject.filter(user_info=user_info.id)
    return [ProjectResult(**project.__dict__) for project in projects]


@pro_router.get("/projects/{project_id}", response_model=ProjectResult, description="获取项目详情")
async def get_project(project_id: int, user_info: Users = Depends(is_authenticated)):
    """获取项目详情"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    return ProjectResult(**project.__dict__)


@pro_router.put("/projects/{project_id}", response_model=ProjectResult, description="更新项目")
async def update_project(project_id: int, item: ProjectParam, user_info: Users = Depends(is_authenticated)):
    """更新项目"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    project.name = item.name
    await project.save()
    return ProjectResult(**project.__dict__)


@pro_router.delete("/projects/{project_id}", description="删除项目", status_code=204)
async def delete_project(project_id: int, user_info: Users = Depends(is_authenticated)):
    """删除项目"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    await project.delete()
    return None


@pro_router.post("/envs", response_model=TestEnvParam, description="创建测试环境", status_code=201)
async def create_env(item: AddEnvParam, user_info: Users = Depends(is_authenticated)):
    """创建测试环境"""
    # env = await TestEnv.create(**item.model_dump())
    project = await TestProject.get_or_none(id=item.project_id)
    if project:
        env = await TestEnv.create(**item.model_dump())
    else:
        raise HTTPException(status_code=405, detail="项目不存在")
    return TestEnvParam(**env.__dict__)


@pro_router.get("/envs", response_model=list[TestEnvParam], description="获取测试环境列表")
async def get_envs(project_id: int, user_info: Users = Depends(is_authenticated)):
    """获取测试环境列表"""
    envs = await TestEnv.filter(project=project_id)
    return [TestEnvParam(**env.__dict__) for env in envs]


@pro_router.get("/envs/{env_id}", response_model=TestEnvParam, description="获取测试环境详情")
async def get_env(env_id: int, user_info: Users = Depends(is_authenticated)):
    """获取测试环境详情"""
    env = await TestEnv.get_or_none(id=env_id)
    if not env:
        raise HTTPException(status_code=405, detail="环境不存在")
    return TestEnvParam(**env.__dict__)


@pro_router.delete("/envs/{env_id}", description="删除测试环境", status_code=204)
async def delete_env(env_id: int, user_info: Users = Depends(is_authenticated)):
    """删除测试环境"""
    env = await TestEnv.get_or_none(id=env_id)
    if not env:
        raise HTTPException(status_code=405, detail="环境不存在")
    await env.delete()
    return None


@pro_router.put("/envs/{env_id}", response_model=TestEnvParam, description="更新测试环境")
async def update_env(env_id: int, item: UpdateEnvParam, user_info: Users = Depends(is_authenticated)):
    """更新测试环境"""
    env = await TestEnv.get_or_none(id=env_id)
    if not env:
        raise HTTPException(status_code=405, detail="环境不存在")
    # env.global_vars = item.global_vars
    # env.host = item.host
    # env.name = item.name
    print("item.model_dump()", item.model_dump())
    update_data = item.model_dump(exclude_unset=True)
    print("aaaa", update_data)
    env = await env.update_from_dict(item.model_dump(exclude_unset=True))
    await env.save()
    return TestEnvParam(**env.__dict__)
