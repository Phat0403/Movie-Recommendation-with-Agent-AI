from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")
    email: str = Field(None, description="The email of the user")
    is_admin: bool = Field(False, description="Is the user an admin")

class UserInDB(User):
    id: int = Field(..., description="The unique identifier of the user")
    username: str = Field(..., description="The username of the user")
    is_admin: bool = Field(False, description="Is the user an admin")
    
    class Config:
        orm_mode = True