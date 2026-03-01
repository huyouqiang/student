"""学生成绩数据模型与 Pydantic 模式。"""

from typing import Optional

from pydantic import BaseModel, Field


class GradeBase(BaseModel):
    """成绩基础模型。"""

    student_id: Optional[int] = Field(None, description="关联学生 ID")
    student_name: str = Field(..., min_length=1, max_length=100, description="学生姓名")
    subject: str = Field(..., min_length=1, max_length=50, description="科目")
    score: float = Field(..., ge=0, le=100, description="分数")
    exam_date: str = Field(default="", max_length=20, description="考试日期")
    semester: str = Field(default="", max_length=50, description="学期")


class GradeCreate(GradeBase):
    """创建成绩请求体。"""

    pass


class GradeUpdate(BaseModel):
    """更新成绩请求体（字段可选）。"""

    student_id: Optional[int] = Field(None)
    student_name: Optional[str] = Field(None, min_length=1, max_length=100)
    subject: Optional[str] = Field(None, min_length=1, max_length=50)
    score: Optional[float] = Field(None, ge=0, le=100)
    exam_date: Optional[str] = Field(None, max_length=20)
    semester: Optional[str] = Field(None, max_length=50)


class Grade(GradeBase):
    """成绩响应模型（含 id）。"""

    id: int = Field(..., description="成绩记录 ID")

    model_config = {"from_attributes": True}
