"""
接口参数的结构体定义
"""
from symtable import Class

from pydantic import BaseModel,Field


class LoginParam(BaseModel):
    """
    登录参数
    """
    username:str= Field( description="用户名",max_length=20,min_length=6)
    password:str= Field( description="密码",max_length=20,min_length=6)

class TokenParamDocs(BaseModel):
    """
    登录参数接口文档使用
    """
    access_token: str=Field( description="访问令牌")
    token_type: str=Field( description="令牌类型")


class RegisterParam(LoginParam):
    """
    注册册数
    """
    password_confirm:str= Field( description="确认密码",max_length=20,min_length=6)
    email: str=Field( description="邮箱",default='')
    mobile:str= Field( description="手机号",default='')
    nickname: str=Field( description="昵称",default='')

class UserInfoParam(BaseModel):
    """
    用户信息参数
    """
    id: int=Field( description="用户id")
    username: str=Field( description="用户名")
    nickname: str=Field( description="昵称",default='')
    mobile: str=Field( description="手机号",default='')
    email: str=Field( description="邮箱",default='')
    is_active: bool=Field( description="是否激活",default=True)
    is_superuser: bool=Field( description="是否是超级用户",default=False)

class LoginResult(BaseModel):
    """
    登录应答参数
    """
    token: str=Field( description="访问令牌")
    user:UserInfoParam

class TokenParam(BaseModel):
    """
    token 参数
    """
    token: str=Field( description="token的值")



