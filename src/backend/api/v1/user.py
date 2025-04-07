from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import User, UserInDB
from services.auth import register_normal_user, login_user
from db.crud_user import UserController
from db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserInDB)
def register_user(user: User, db: Session = Depends(get_db)):
    return register_normal_user(UserController(db), user.username, user.password)

@router.post("/login", response_model=UserInDB)
def login_user(user: User, db: Session = Depends(get_db)):
    user_controller = UserController(db)
    response = login_user(user_controller, user.username, user.password)
    if isinstance(response, str):
        return {"error": response}
    return response