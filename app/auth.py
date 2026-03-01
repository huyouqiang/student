"""简单会话与管理员鉴权（session + 角色）。"""

import hashlib
import os
from typing import Annotated

from fastapi import Depends, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse, RedirectResponse

# 管理员账号（演示用，密码为 admin123）
ADMIN_USERNAME = "admin"
_ADMIN_PASSWORD_SALT = "student-admin"
_ADMIN_PASSWORD_HASH = hashlib.sha256(
    (_ADMIN_PASSWORD_SALT + "admin123").encode()
).hexdigest()


def _hash_password(password: str) -> str:
    return hashlib.sha256((_ADMIN_PASSWORD_SALT + password).encode()).hexdigest()


def verify_admin(username: str, password: str) -> bool:
    """校验是否为管理员账号。"""
    return (
        username == ADMIN_USERNAME and _hash_password(password) == _ADMIN_PASSWORD_HASH
    )


def get_current_user(request: Request) -> dict:
    """从 session 获取当前用户，未登录视为访客。"""
    role = request.session.get("role", "guest")
    username = request.session.get("username", "")
    return {"username": username, "role": role}


def require_admin(
    request: Request,
    user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """依赖：仅管理员可过，否则 403。"""
    if user.get("role") != "admin":
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="需要管理员权限")
    return user


PUBLIC_PATHS = {"/", "/login"}


class LoginRequiredMiddleware(BaseHTTPMiddleware):
    """未登录用户只能访问首页和登录页，其他请求重定向到登录或返回 401。"""

    async def dispatch(self, request, call_next):
        path = request.url.path
        if path in PUBLIC_PATHS:
            return await call_next(request)
        role = request.session.get("role", "guest")
        if role != "admin":
            if path.startswith("/api/"):
                return JSONResponse(
                    status_code=401,
                    content={"detail": "需要登录"},
                )
            return RedirectResponse(url="/login", status_code=302)
        return await call_next(request)


def init_session_middleware(app) -> None:
    """为 app 注册 Session 与登录校验中间件。"""
    app.add_middleware(LoginRequiredMiddleware)
    secret = os.environ.get("SESSION_SECRET", "dev-secret-change-in-production")
    app.add_middleware(SessionMiddleware, secret_key=secret)
