"""用户登录与登出（从 users 表校验）。"""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user, verify_user

router = APIRouter(tags=["认证"])
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent.parent / "templates")
)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    """登录页。"""
    user = get_current_user(request)
    if user.get("role") is not None:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request, "is_admin": False, "is_logged_in": False},
    )


@router.post("/login")
def login_submit(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
) -> RedirectResponse:
    """提交登录表单。"""
    username = (username or "").strip()
    if not username:
        return RedirectResponse(
            url="/login?error=empty",
            status_code=302,
        )
    user = verify_user(username, password)
    if user:
        request.session["username"] = user["name"]
        request.session["role"] = user["role"]
        return RedirectResponse(url="/", status_code=302)
    return RedirectResponse(
        url="/login?error=invalid",
        status_code=302,
    )


@router.post("/logout")
def logout(request: Request) -> RedirectResponse:
    """登出，清除 session。"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=302)
