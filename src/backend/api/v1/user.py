from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from schemas.user import User, UserInDB
from services.auth import register_normal_user, login_user
from db.crud_user import UserController
from db.session import get_db
from services.auth import AuthService

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user(user: User, db: Session = Depends(get_db)):
    user_controller = UserController(db)
    auth_service = AuthService(user_controller)
    response = register_normal_user(auth_service, user.username, user.password)
    if isinstance(response, str):
        return JSONResponse(
            status_code=400,
            content={"error": response}
        )
    return JSONResponse(
        status_code=201,
        content={"message": "User registered successfully", "user": response}
    )

@router.post("/login", response_model=UserInDB)
def login_user(user: User, db: Session = Depends(get_db)):
    user_controller = UserController(db)
    auth_service = AuthService(user_controller)
    response = auth_service.login_user(user.username, user.password)
    if isinstance(response, str):
        return {"error": response}
    return JSONResponse(
        status_code=200,
        content={"message": "Login successful", "access_token": response["access_token"]},
    )