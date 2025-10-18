"""接口函数定义"""

from fastapi import APIRouter, HTTPException
from fastapi.openapi.models import OAuth2
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.users.parameter import RegisterParam, LoginParam, UserInfoParam, LoginResult, TokenParam, TokenParamDocs
from apps.users.models import Users
from comms.auth import get_password_hash, verify_password, create_token, verify_token

user_router = APIRouter(prefix="/api/users", tags=["用户管理"])


@user_router.post("/register", description="用户注册", response_model=UserInfoParam)
async def register(item: RegisterParam):
    if item.password != item.password_confirm:
        raise HTTPException(status_code=400, detail="密码不一致")
    elif await Users.get_or_none(username=item.username):
        raise HTTPException(status_code=400, detail="用户已存在")
    else:
        # 生成密码的hash值
        passwd=get_password_hash(item.password)
        # 创建用户
        user = await Users.create(username=item.username, password=passwd
                            , nickname=item.nickname, email=item.email, mobile=item.mobile)
        return UserInfoParam(**user.__dict__)


@user_router.post("/login", description="用户登录", response_model=LoginResult)
async def login(item: LoginParam):
    user=await Users.get_or_none(username=item.username)
    if user:
        res=verify_password(item.password, user.password)
        if res:
            # 生成token
            user_info=UserInfoParam(**user.__dict__)
            token=create_token(user_info.model_dump())
            return LoginResult(token=token,user=user_info)
        else:
            raise HTTPException(status_code=400, detail="密码错误")
    else:
        raise HTTPException(status_code=400, detail="用户不存在")

@user_router.post("/login_docs", description="用户登录接口文档调用", response_model=TokenParamDocs)
async def login_docs(item: OAuth2PasswordRequestForm=Depends()):
    """
    用户登录接口文档调用
    :param item: 登录参数
    :return: token
    """
    user = await Users.get_or_none(username=item.username)
    if user:
        res = verify_password(item.password, user.password)
        if res:
            # 生成token
            user_info = UserInfoParam(**user.__dict__)
            token = create_token(user_info.model_dump())
            return TokenParamDocs(access_token=token, token_type="Bearer")
        else:
            raise HTTPException(status_code=400, detail="密码错误")
    else:
        raise HTTPException(status_code=400, detail="用户不存在")
# token校验
@user_router.post("/verify", description="token校验", response_model=LoginResult)
async def token_verify(item: TokenParam):
    user=verify_token(item.token)
    return LoginResult(token=item.token,user=UserInfoParam(**user))

# token刷新
@user_router.post("/refresh", description="token刷新", response_model=LoginResult)
async def token_refresh(item: TokenParam):
    user=verify_token(item.token)
    user_info=UserInfoParam(**user)
    token=create_token(user_info.model_dump())
    return LoginResult(token=token,user=user_info)