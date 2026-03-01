"""学生成绩增删改查 API。"""

from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import require_root
from app.models.grade import grade_store
from app.schemas.grade import Grade, GradeCreate, GradeUpdate

router = APIRouter(prefix="/api/grades", tags=["学生成绩"])


@router.get("")
def list_grades(
    student_id: Optional[int] = Query(None, description="按学生 ID 筛选"),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=50),
) -> Union[dict, list]:
    """获取成绩列表（访客可查看）。按 student_id 筛选时返回全部；否则分页。"""
    if student_id is not None:
        return grade_store.get_all(student_id=student_id)
    total = grade_store.get_count()
    offset = (page - 1) * limit
    items = grade_store.get_page(offset, limit, student_id=None)
    return {"items": items, "total": total, "page": page, "per_page": limit}


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
    _admin: Annotated[dict, Depends(require_root)],
) -> dict:
    """新增成绩（仅管理员）。"""
    return grade_store.create(data)


@router.put("/{grade_id}", response_model=Grade)
def update_grade(
    grade_id: int,
    data: GradeUpdate,
    _admin: Annotated[dict, Depends(require_root)],
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
    _admin: Annotated[dict, Depends(require_root)],
) -> None:
    """删除成绩（仅管理员）。"""
    if not grade_store.delete(grade_id):
        raise HTTPException(status_code=404, detail="成绩记录不存在")
