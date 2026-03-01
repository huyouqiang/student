"""学生数据模型与 Pydantic 模式。"""

from typing import Optional

from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    """学生基础模型。"""

    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    age: int = Field(..., ge=1, le=150, description="年龄")
    grade: str = Field(default="", max_length=50, description="年级/班级")


class StudentCreate(StudentBase):
    """创建学生请求体。"""

    pass


class StudentUpdate(BaseModel):
    """更新学生请求体（字段可选）。"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=1, le=150)
    grade: Optional[str] = Field(None, max_length=50)


class Student(StudentBase):
    """学生响应模型（含 id）。"""

    id: int = Field(..., description="学生 ID")

    model_config = {"from_attributes": True}
