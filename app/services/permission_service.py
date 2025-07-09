from fastapi import HTTPException, status
from models import Permission, Task, User

class PermissionService:
    @staticmethod
    async def get_task_permissions(task_id: int, current_user: User) -> list:
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            raise HTTPException(status_code=403, detail="Только владелец задачи может просматривать разрешения")

        permissions = await Permission.filter(task_id=task_id).prefetch_related("user")
        return permissions

    @staticmethod
    async def create_task_permission(task_id: int, user_id: int, can_read: bool, can_update: bool, current_user: User) -> Permission:
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            raise HTTPException(status_code=403, detail="Только владелец задачи может создавать разрешения")

        target_user = await User.get_or_none(id=user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="Целевой пользователь не найден")

        if await Permission.filter(user=target_user, task_id=task_id).exists():
            raise HTTPException(status_code=400, detail="Разрешение уже существует для этого пользователя и задачи")

        permission = await Permission.create(
            user=target_user,
            task_id=task_id,
            can_read=can_read,
            can_update=can_update
        )
        return permission

    @staticmethod
    async def update_task_permission(task_id: int, permission_id: int, user_id: int, can_read: bool, can_update: bool, current_user: User) -> Permission:
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            raise HTTPException(status_code=403, detail="Обновлять разрешения может только владелец задачи")

        permission = await Permission.get_or_none(id=permission_id, task_id=task_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Разрешение не найдено")

        target_user = await User.get_or_none(id=user_id)
        if not target_user:
            raise HTTPException(status_code=404, detail="Целевой пользователь не найден")

        permission.user = target_user
        permission.can_read = can_read
        permission.can_update = can_update
        await permission.save()
        return permission

    @staticmethod
    async def delete_task_permission(task_id: int, permission_id: int, current_user: User):
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            raise HTTPException(status_code=403, detail="Удалять разрешения может только владелец задачи")

        permission = await Permission.get_or_none(id=permission_id, task_id=task_id)
        if not permission:
            raise HTTPException(status_code=404, detail="Разрешение не найдено")

        await permission.delete()
        return {"message": "Разрешение успешно удалено"}