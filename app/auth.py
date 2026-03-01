"""会话与用户鉴权（session + users 表，role 0=根用户 1=访客）。"""

import hashlib
import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse, RedirectResponse

_PASSWORD_SALT = "student-admin"


def _hash_password(password: str) -> str:
    return hashlib.sha256((_PASSWORD_SALT + password).encode()).hexdigest()


def verify_user(username: str, password: str) -> Optional[dict]:
    """校验用户，返回 {id, name, role} 或 None。"""
    from app.models.user import user_store

    h = _hash_password(password)
    return user_store.verify(username, h)


def get_current_user(request: Request) -> dict:
    """从 session 获取当前用户。role: 0=根用户, 1=访客, None=未登录。"""
    role = request.session.get("role")
    username = request.session.get("username", "")
    return {"username": username, "role": role}


def require_root(
    user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    """依赖：仅 role=0 根用户可过，否则 403。"""
    if user.get("role") != 0:
        raise HTTPException(status_code=403, detail="需要根用户权限")
    return user


PUBLIC_PATHS = {"/", "/login"}


class LoginRequiredMiddleware(BaseHTTPMiddleware):
    """未登录用户只能访问首页和登录页。"""

    async def dispatch(self, request, call_next):
        path = request.url.path
        if path in PUBLIC_PATHS:
            return await call_next(request)
        role = request.session.get("role")
        if role is None:
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
