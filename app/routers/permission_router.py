from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Permission, Task, User
from core.security import get_current_user
from schemas import PermissionResponse, PermissionCreateUpdate
from services.permission_service import PermissionService

router = APIRouter()

@router.get("/{task_id}/permissions", response_model=List[PermissionResponse])
async def get_task_permissions(task_id: int, current_user: User = Depends(get_current_user)):
    permissions = await PermissionService.get_task_permissions(task_id, current_user)
    return [PermissionResponse.from_orm(p) for p in permissions]

@router.post("/{task_id}/permissions", response_model=PermissionResponse)
async def create_task_permission(
    task_id: int,
    permission_data: PermissionCreateUpdate,
    current_user: User = Depends(get_current_user)
):
    permission = await PermissionService.create_task_permission(
        task_id,
        permission_data.user_id,
        permission_data.can_read,
        permission_data.can_update,
        current_user
    )
    return PermissionResponse.from_orm(permission)

@router.put("/{task_id}/permissions/{permission_id}", response_model=PermissionResponse)
async def update_task_permission(
    task_id: int,
    permission_id: int,
    permission_data: PermissionCreateUpdate,
    current_user: User = Depends(get_current_user)
):
    permission = await PermissionService.update_task_permission(
        task_id,
        permission_id,
        permission_data.user_id,
        permission_data.can_read,
        permission_data.can_update,
        current_user
    )
    return PermissionResponse.from_orm(permission)

@router.delete("/{task_id}/permissions/{permission_id}")
async def delete_task_permission(
    task_id: int,
    permission_id: int,
    current_user: User = Depends(get_current_user)
):
    result = await PermissionService.delete_task_permission(task_id, permission_id, current_user)
    return JSONResponse(content=result)