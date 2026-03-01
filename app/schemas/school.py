"""学校数据模型与 Pydantic 模式。"""

from typing import Optional

from pydantic import BaseModel, Field


class SchoolBase(BaseModel):
    """学校基础模型。"""

    name: str = Field(..., min_length=1, max_length=100, description="学校名称")
    address: str = Field(default="", max_length=200, description="地址")
    school_type: str = Field(default="", max_length=20, description="类型：小学/初中/高中")
    student_count: int = Field(default=0, ge=0, description="学生人数")


class SchoolCreate(SchoolBase):
    """创建学校请求体。"""

    pass


class SchoolUpdate(BaseModel):
    """更新学校请求体（字段可选）。"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    school_type: Optional[str] = Field(None, max_length=20)
    student_count: Optional[int] = Field(None, ge=0)


class School(SchoolBase):
    """学校响应模型（含 id）。"""

    id: int = Field(..., description="学校 ID")

    model_config = {"from_attributes": True}
