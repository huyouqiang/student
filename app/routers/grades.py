"""学生成绩增删改查 API。"""

from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import require_admin
from app.models.grade import grade_store
from app.schemas.grade import Grade, GradeCreate, GradeUpdate

router = APIRouter(prefix="/api/grades", tags=["学生成绩"])


@router.get("", response_model=List[Grade])
def list_grades(
    student_id: Optional[int] = Query(None, description="按学生 ID 筛选"),
) -> list:
    """获取成绩列表（访客可查看），支持按 student_id 筛选。"""
    return grade_store.get_all(student_id=student_id)


@router.get("/{grade_id}", response_model=Grade)
def get_grade(grade_id: int) -> dict:
    """根据 id 获取单条成绩（访客可查看）。"""
    grade = grade_store.get_by_id(grade_id)
    if grade is None:
        raise HTTPException(status_code=404, detail="成绩记录不存在")
    return grade


@router.post("", response_model=Grade, status_code=201)
def create_grade(
    data: GradeCreate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """新增成绩（仅管理员）。"""
    return grade_store.create(data)


@router.put("/{grade_id}", response_model=Grade)
def update_grade(
    grade_id: int,
    data: GradeUpdate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """更新成绩（仅管理员）。"""
    update_dict = data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="未提供要更新的字段")
    grade = grade_store.update(grade_id, update_dict)
    if grade is None:
        raise HTTPException(status_code=404, detail="成绩记录不存在")
    return grade


@router.delete("/{grade_id}", status_code=204)
def delete_grade(
    grade_id: int,
    _admin: Annotated[dict, Depends(require_admin)],
) -> None:
    """删除成绩（仅管理员）。"""
    if not grade_store.delete(grade_id):
        raise HTTPException(status_code=404, detail="成绩记录不存在")
