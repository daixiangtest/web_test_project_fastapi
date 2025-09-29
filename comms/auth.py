"""
用户认证和登录的权限校验和token的生成与验证
"""

import time
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from apps.users.models import Users
from comms.settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# fastAPI 默认的请求登录接口的方法
oatu2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

async def is_authenticated(token: str = Depends(oatu2_scheme)):
    """
    获取当前用户
    :param token: 登录的token信息
    :return: 用户信息的对象
    """
    # 验证token信息获取信息
    user_id=verify_token(token).get("id")
    # 根据用户id查询用户信息
    user =await Users.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


def get_password_hash(password):
    """
    获取密码的hash值
    :param password: 明文密码
    :return: 密文密码
    """
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception as e:
        raise HTTPException(status_code=401, detail="密码加密失败")
def verify_password(plain_password, hashed_password):
    """
    验证密码
    :param plain_password: 明文密码
    :param hashed_password: 密文密码
    :return:
    """
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        raise HTTPException(status_code=401, detail="密码验证失败")
def create_token(token_data: dict):
    """
    创建token
    :param token_data:
    :return:
    """
    try:
        secret_key = SECRET_KEY
        token_data.update({"exp": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES})
        token_value = jwt.encode(token_data, secret_key, algorithm="HS256")
        return token_value
    except Exception as e:
        raise HTTPException(status_code=401, detail="token生成失败")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
def verify_token(token_value: str = Depends(oauth2_scheme)):
    """
    校验token是否有效
    :param token_value:
    :return: 解析后的token信息
    """
    secret_key = SECRET_KEY
    try:
        token_data = jwt.decode(token_value, secret_key, algorithms=["HS256"])
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail="token验证失败")


if __name__ == '__main__':
    data = {"id": 1, "name": "dx"}
    token = create_token(data)
    print(token)
    time.sleep(2)
    print(verify_token(token))
