"""学生列表增删改查 API。"""

from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import require_root
from app.models.student import student_store
from app.schemas.student import Student, StudentCreate, StudentUpdate

router = APIRouter(prefix="/api/students", tags=["学生"])


@router.get("")
def list_students(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=50),
    all_items: bool = Query(False, alias="all", description="返回全部不分页"),
    search: Optional[str] = Query(None, description="按姓名或年级搜索"),
) -> Union[dict, list]:
    """获取学生列表（访客可查看，分页）。"""
    if all_items:
        return student_store.get_all()
    keyword = search.strip() if search and search.strip() else None
    if keyword:
        total = student_store.search_count(keyword)
        offset = (page - 1) * limit
        items = student_store.search_page(offset, limit, keyword)
    else:
        total = student_store.get_count()
        offset = (page - 1) * limit
        items = student_store.get_page(offset, limit)
    return {"items": items, "total": total, "page": page, "per_page": limit}


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
    _admin: Annotated[dict, Depends(require_root)],
) -> dict:
    """新增学生（仅管理员）。"""
    return student_store.create(data)


@router.put("/{student_id}", response_model=Student)
def update_student(
    student_id: int,
    data: StudentUpdate,
    _admin: Annotated[dict, Depends(require_root)],
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
    _admin: Annotated[dict, Depends(require_root)],
) -> None:
    """删除学生（仅管理员）。"""
    if not student_store.delete(student_id):
        raise HTTPException(status_code=404, detail="学生不存在")
