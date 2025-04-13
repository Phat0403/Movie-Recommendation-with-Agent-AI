from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud_user import UserController
from db.session import get_db
from schemas.user import User, UserInDB
from services.auth import AuthService
from db.redis_client import RedisClient

from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

def get_user_controller(db: Session = Depends(get_db)):
    return UserController(db)

def get_auth_service(user_controller: UserController = Depends(get_user_controller)):
    return AuthService(user_controller)

def get_redis_client():
    return RedisClient()

@router.get("/me", response_model=UserInDB)
def get_current_user(auth_service: AuthService = Depends(get_auth_service), token: str = Depends(OAuth2PasswordBearer(tokenUrl="api/v1/users/login"))):
    user = auth_service.get_current_user_by_token(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/register", response_model=UserInDB)
def register_user(user: User, auth_service: AuthService = Depends(get_auth_service)):
    logger.debug(user)
    response = auth_service.register_user(user.username, user.password, user.email, user.is_admin)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/login", response_model=UserInDB)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)):
    response = auth_service.login_user(form_data.username, form_data.password)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/send_verification_code")
async def send_verification_code(username: str, auth_service: AuthService = Depends(get_auth_service), redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.send_email_verification(redis_client, username)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/reset_password")
async def reset_password(code: str, username: str, new_password: str, auth_service: AuthService = Depends(get_auth_service), redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.verify_password_reset_code(redis_client, username, code)

    if response.get("status") != 200:
        return JSONResponse(content=response, status_code=response.get("status", 400))
    
    response = auth_service.reset_password(username, new_password)
    return JSONResponse(content=response, status_code=response.get("status", 200))