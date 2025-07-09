from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models import Task, User
from core.security import get_current_user
from schemas import TaskCreate, TaskUpdate, TaskResponse
from services.task_service import TaskService

router = APIRouter()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(current_user: User = Depends(get_current_user)):
    tasks = await TaskService.get_user_tasks(current_user)
    return [TaskResponse.from_orm(task) for task in tasks]

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, current_user: User = Depends(get_current_user)):
    task = await TaskService.get_task(task_id, current_user)
    return TaskResponse.from_orm(task)

@router.post("/", response_model=TaskResponse)
async def create_task(task_data: TaskCreate, current_user: User = Depends(get_current_user)):
    task = await TaskService.create_task(task_data, current_user)
    return TaskResponse.from_orm(task)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    task = await TaskService.update_task(task_id, task_data, current_user)
    return TaskResponse.from_orm(task)

@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    result = await TaskService.delete_task(task_id, current_user)
    return JSONResponse(content=result)