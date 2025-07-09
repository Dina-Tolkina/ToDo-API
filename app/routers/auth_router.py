from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from core.security import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    user = await UserService.get_user_by_login(user_data.login)
    if user:
        raise HTTPException(status_code=400, detail="Логин уже зарегистрирован")
    user = await UserService.create_user(user_data)
    return user

@router.post("/login", response_model=dict)
async def login_for_access_token(user_data: UserLogin):
    user = await UserService.get_user_by_login(user_data.login)
    if not user or not UserService.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.login}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}