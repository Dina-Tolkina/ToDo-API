from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    login: str
    password: str

class UserLogin(BaseModel):
    login: str
    password: str

class UserResponse(BaseModel):
    id: int
    login: str

    class Config:
        from_attributes = True


class PermissionCreateUpdate(BaseModel):
    user_id: int
    can_read: bool
    can_update: bool


class PermissionResponse(BaseModel):
    id: int
    user_id: int
    task_id: int
    can_read: bool
    can_update: bool

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    title: str
    description: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True