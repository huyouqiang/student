"""教师数据模型与 Pydantic 模式。"""

from typing import Optional

from pydantic import BaseModel, Field


class TeacherBase(BaseModel):
    """教师基础模型。"""

    name: str = Field(..., min_length=1, max_length=100, description="姓名")
    subject: str = Field(default="", max_length=50, description="任教科目")
    title: str = Field(default="", max_length=50, description="职称")
    phone: str = Field(default="", max_length=20, description="联系电话")


class TeacherCreate(TeacherBase):
    """创建教师请求体。"""

    pass


class TeacherUpdate(BaseModel):
    """更新教师请求体（字段可选）。"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    subject: Optional[str] = Field(None, max_length=50)
    title: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)


class Teacher(TeacherBase):
    """教师响应模型（含 id）。"""

    id: int = Field(..., description="教师 ID")

    model_config = {"from_attributes": True}
