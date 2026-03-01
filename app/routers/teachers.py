"""教师列表增删改查 API。"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import require_admin
from app.models.teacher import teacher_store
from app.schemas.teacher import Teacher, TeacherCreate, TeacherUpdate

router = APIRouter(prefix="/api/teachers", tags=["教师"])


@router.get("")
def list_teachers(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=50),
) -> dict:
    """获取教师列表（访客可查看，分页）。"""
    total = teacher_store.get_count()
    offset = (page - 1) * limit
    items = teacher_store.get_page(offset, limit)
    return {"items": items, "total": total, "page": page, "per_page": limit}


@router.get("/{teacher_id}", response_model=Teacher)
def get_teacher(teacher_id: int) -> dict:
    """根据 id 获取单个教师（访客可查看）。"""
    teacher = teacher_store.get_by_id(teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="教师不存在")
    return teacher


@router.post("", response_model=Teacher, status_code=201)
def create_teacher(
    data: TeacherCreate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """新增教师（仅管理员）。"""
    return teacher_store.create(data)


@router.put("/{teacher_id}", response_model=Teacher)
def update_teacher(
    teacher_id: int,
    data: TeacherUpdate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """更新教师（仅管理员）。"""
    update_dict = data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="未提供要更新的字段")
    teacher = teacher_store.update(teacher_id, update_dict)
    if teacher is None:
        raise HTTPException(status_code=404, detail="教师不存在")
    return teacher


@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(
    teacher_id: int,
    _admin: Annotated[dict, Depends(require_admin)],
) -> None:
    """删除教师（仅管理员）。"""
    if not teacher_store.delete(teacher_id):
        raise HTTPException(status_code=404, detail="教师不存在")
