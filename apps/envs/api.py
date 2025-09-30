"""接口函数定义"""

from fastapi import APIRouter, HTTPException, Depends
from apps.projects.parameter import ProjectParam,ProjectResult
from apps.projects.models import TestProject
from apps.users.models import Users
from comms.auth import is_authenticated

pro_router=APIRouter(prefix="/api/env",tags=["环境管理"])

