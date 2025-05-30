from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.crud_user import UserController
from db.redis_client import RedisClient
from db.clients import get_redis_client, get_db

from schemas.user import User, UserInDB

from services.auth import AuthService

from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# Initialize the dependencies only once
db: Session = next(get_db())  # Get the database session
user_controller = UserController(db)
auth_service = AuthService(user_controller)

# Routes
@router.get("/me", response_model=UserInDB)
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/initiate-registration")
async def initiate_registration(user: User, redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.send_register_otp_email(username=user.username, password=user.password, email=user.email, redis_client=redis_client)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/verify-otp-and-register")
async def verify_otp_and_register(username: str, code: str, redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.register(otp=code, username=username, redis_client=redis_client)
    
    if response.get("status") != 200:
        return JSONResponse(content=response, status_code=response.get("status", 400))
    
    return JSONResponse(content="Registration successful", status_code=200)

@router.post("/resend-registration-otp")
async def resend_registration_otp(username: str, redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.resend_registration_otp(username=username, redis_client=redis_client)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/login", response_model=UserInDB)
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    response = auth_service.login(form_data.username, form_data.password)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/send-verification-code")
async def send_verification_code(username: str, redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.send_password_reset_email(redis_client, username)
    return JSONResponse(content=response, status_code=response.get("status", 200))

@router.post("/reset-password")
async def reset_password(code: str, username: str, new_password: str, redis_client: RedisClient = Depends(get_redis_client)):
    response = await auth_service.verify_password_reset_code(redis_client, username, code)

    if response.get("status") != 200:
        return JSONResponse(content=response, status_code=response.get("status", 400))
    
    response = auth_service.reset_password(username, new_password)
    return JSONResponse(content=response, status_code=response.get("status", 200))
