"""学校列表增删改查 API。"""

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_admin
from app.models.school import school_store
from app.schemas.school import School, SchoolCreate, SchoolUpdate

router = APIRouter(prefix="/api/schools", tags=["学校"])


@router.get("", response_model=List[School])
def list_schools() -> list:
    """获取学校列表（访客可查看）。"""
    return school_store.get_all()


@router.get("/{school_id}", response_model=School)
def get_school(school_id: int) -> dict:
    """根据 id 获取单个学校（访客可查看）。"""
    school = school_store.get_by_id(school_id)
    if school is None:
        raise HTTPException(status_code=404, detail="学校不存在")
    return school


@router.post("", response_model=School, status_code=201)
def create_school(
    data: SchoolCreate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """新增学校（仅管理员）。"""
    return school_store.create(data)


@router.put("/{school_id}", response_model=School)
def update_school(
    school_id: int,
    data: SchoolUpdate,
    _admin: Annotated[dict, Depends(require_admin)],
) -> dict:
    """更新学校（仅管理员）。"""
    update_dict = data.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(status_code=400, detail="未提供要更新的字段")
    school = school_store.update(school_id, update_dict)
    if school is None:
        raise HTTPException(status_code=404, detail="学校不存在")
    return school


@router.delete("/{school_id}", status_code=204)
def delete_school(
    school_id: int,
    _admin: Annotated[dict, Depends(require_admin)],
) -> None:
    """删除学校（仅管理员）。"""
    if not school_store.delete(school_id):
        raise HTTPException(status_code=404, detail="学校不存在")
