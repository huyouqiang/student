"""学生列表增删改查 API。"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_admin
from app.models.student import student_store
from app.schemas.student import Student, StudentCreate, StudentUpdate

router = APIRouter(prefix="/api/students", tags=["学生"])


@router.get("", response_model=List[Student])
def list_students() -> list:
    """获取学生列表（访客可查看）。"""
    return student_store.get_all()


@router.get("/{student_id}", response_model=Student)
def get_student(student_id: int) -> dict:
    """根据 id 获取单个学生（访客可查看）。"""
    student = student_store.get_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="学生不存在")
    return student


@router.post("", response_model=Student, status_code=201)
def create_student(
    data: StudentCreate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """新增学生（仅管理员）。"""
    return student_store.create(data)


@router.put("/{student_id}", response_model=Student)
def update_student(
    student_id: int,
    data: StudentUpdate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """更新学生（仅管理员）。"""
    update_dict = data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="未提供要更新的字段")
    student = student_store.update(student_id, update_dict)
    if student is None:
        raise HTTPException(status_code=404, detail="学生不存在")
    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    _admin: Annotated[dict, Depends(require_admin)],
) -> None:
    """删除学生（仅管理员）。"""
    if not student_store.delete(student_id):
        raise HTTPException(status_code=404, detail="学生不存在")
