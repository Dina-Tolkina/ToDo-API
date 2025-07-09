from passlib.context import CryptContext
from models import User
from schemas import UserCreate
from models import Permission
from schemas import PermissionResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    async def get_user_by_login(login: str):
        return await User.get_or_none(login=login)

    @staticmethod
    async def create_user(user_data: UserCreate):
        hashed_password = pwd_context.hash(user_data.password)
        user = await User.create(login=user_data.login, hashed_password=hashed_password)
        return user

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    async def get_user_by_id(user_id: int) -> User:
        return await User.get(id=user_id).prefetch_related('permissions')

