"""FastAPI 应用入口：学生列表增删改查。"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.auth import get_current_user, init_session_middleware
from app.database import init_db
from app.routers import auth, grades, schools, students, teachers

app = FastAPI(
    title="学生管理 API",
    description="学生列表的增删改查接口",
    version="1.0.0",
)

init_session_middleware(app)


@app.on_event("startup")
def startup() -> None:
    """应用启动时初始化 MySQL 数据库和表。"""
    init_db()


templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(schools.router)
app.include_router(grades.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    """首页。"""
    user = get_current_user(request)
    is_admin = user.get("role") == "admin"
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "is_admin": is_admin},
    )


@app.get("/students", response_class=HTMLResponse)
def students_page(request: Request) -> HTMLResponse:
    """学生列表页面。"""
    user = get_current_user(request)
    is_admin = user.get("role") == "admin"
    return templates.TemplateResponse(
        "students/index.html",
        {"request": request, "is_admin": is_admin},
    )


@app.get("/teachers", response_class=HTMLResponse)
def teachers_page(request: Request) -> HTMLResponse:
    """教师列表页面。"""
    user = get_current_user(request)
    is_admin = user.get("role") == "admin"
    return templates.TemplateResponse(
        "teachers/index.html",
        {"request": request, "is_admin": is_admin},
    )


@app.get("/schools", response_class=HTMLResponse)
def schools_page(request: Request) -> HTMLResponse:
    """学校列表页面。"""
    user = get_current_user(request)
    is_admin = user.get("role") == "admin"
    return templates.TemplateResponse(
        "schools/index.html",
        {"request": request, "is_admin": is_admin},
    )


@app.get("/grades", response_class=HTMLResponse)
def grades_page(request: Request) -> HTMLResponse:
    """学生成绩页面。"""
    user = get_current_user(request)
    is_admin = user.get("role") == "admin"
    return templates.TemplateResponse(
        "grades/index.html",
        {"request": request, "is_admin": is_admin},
    )


@app.get("/api-info")
def api_info() -> dict:
    """API 说明。"""
    return {
        "message": "学生管理 API",
        "docs": "/docs",
        "students": "/api/students",
        "teachers": "/api/teachers",
        "schools": "/api/schools",
        "grades": "/api/grades",
    }
