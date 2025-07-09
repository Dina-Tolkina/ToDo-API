from fastapi import HTTPException, status
from models import Permission, Task, User
from schemas import TaskCreate, TaskUpdate

class TaskService:
    @staticmethod
    async def get_user_tasks(current_user: User) -> list:
        owner_tasks = await Task.filter(owner=current_user).prefetch_related("owner")
        permitted_tasks = await Task.filter(permissions__user=current_user, permissions__can_read=True).prefetch_related("owner")
        return list(set(owner_tasks + permitted_tasks))  

    @staticmethod
    async def get_task(task_id: int, current_user: User) -> Task:
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            permission = await Permission.get_or_none(user=current_user, task_id=task_id, can_read=True)
            if not permission:
                raise HTTPException(status_code=403, detail="Нет прав на просмотр этой задачи")
        
        return task

    @staticmethod
    async def create_task(task_data: TaskCreate, current_user: User) -> Task:
        if len(task_data.title) > 100:
            raise HTTPException(status_code=400, detail="Заголовок задачи не может превышать 100 символов")
        
        task = await Task.create(
            title=task_data.title,
            description=task_data.description,
            owner=current_user
        )
        return task

    @staticmethod
    async def update_task(task_id: int, task_data: TaskUpdate, current_user: User) -> Task:
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            permission = await Permission.get_or_none(user=current_user, task_id=task_id, can_update=True)
            if not permission:
                raise HTTPException(status_code=403, detail="Нет прав на обновление этой задачи")

        if task_data.title is not None:
            if len(task_data.title) > 100:
                raise HTTPException(status_code=400, detail="Заголовок задачи не может превышать 100 символов")
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        
        await task.save()
        return task

    @staticmethod
    async def delete_task(task_id: int, current_user: User):
        task = await Task.get_or_none(id=task_id).prefetch_related("owner")
        if not task:
            raise HTTPException(status_code=404, detail="Задание не найдено")
        
        if task.owner != current_user:
            raise HTTPException(status_code=403, detail="Только владелец задачи может её удалить")
        
        await task.delete()
        return {"message": "Задание успешно удалено"}