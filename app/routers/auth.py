"""管理员登录与登出。"""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user, verify_admin

router = APIRouter(tags=["认证"])
templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.parent.parent / "templates")
)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request) -> HTMLResponse:
    """登录页。"""
    user = get_current_user(request)
    if user.get("role") == "admin":
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request, "is_admin": False},
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
    if verify_admin(username, password):
        request.session["username"] = username
        request.session["role"] = "admin"
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
