"""接口函数定义"""

from fastapi import APIRouter, HTTPException, Depends
from apps.projects.parameter import ProjectParam,ProjectResult
from apps.projects.models import TestProject
from apps.users.models import Users
from comms.auth import is_authenticated

pro_router=APIRouter(prefix="/api/pro",tags=["项目管理"])

@pro_router.post("/projects",response_model=ProjectResult,description="创建项目")
async def create_project(item: ProjectParam,user_info: Users = Depends(is_authenticated)):
    """创建项目"""
    project = await TestProject.create(name=item.name, user_info=user_info)
    return ProjectResult(**project.__dict__)

@pro_router.get("/projects",response_model=list[ProjectResult],description="获取项目列表")
async def get_projects(user_info: Users = Depends(is_authenticated)):
    """获取项目列表"""
    # 通过用户id项目列表
    projects = await TestProject.filter(user_info=user_info.id)
    return [ProjectResult(**project.__dict__) for project in projects]

@pro_router.get("/projects/{project_id}",response_model=ProjectResult,description="获取项目详情")
async def get_project(project_id: int,user_info: Users = Depends(is_authenticated)):
    """获取项目详情"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    return ProjectResult(**project.__dict__)

@pro_router.put("/projects/{project_id}",response_model=ProjectResult,description="更新项目")
async def update_project(project_id: int,item: ProjectParam,user_info: Users = Depends(is_authenticated)):
    """更新项目"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    project.name = item.name
    await project.save()
    return ProjectResult(**project.__dict__)

@pro_router.delete("/projects/{project_id}",description="删除项目",status_code=204)
async def delete_project(project_id: int,user_info: Users = Depends(is_authenticated)):
    """删除项目"""
    project = await TestProject.get(id=project_id, user_info_id=user_info.id)
    await project.delete()
    return None