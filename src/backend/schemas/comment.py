from pydantic import BaseModel, Field
from datetime import datetime
class Comment(BaseModel):
    id: int = Field(..., description="The unique identifier of the comment")
    movie_id: str = Field(..., description="The ID of the movie associated with the comment")
    username: str = Field(..., description="The ID of the user who made the comment")
    comment: str = Field(..., description="The content of the comment")
    comment_time: datetime = Field(..., description="The time when the comment was made")

    class Config:
        from_attributes = True

class CommentList(BaseModel):
    comments: list[Comment] = Field(..., description="A list of comments")

class CommentCreate(BaseModel):
    movie_id: str = Field(..., description="The ID of the movie for which the comment is being created")
    comment_text: str = Field(..., description="The content of the comment")

class CommentUpdate(BaseModel):
    comment_id: int = Field(..., description="The unique identifier of the comment to be updated")
    comment_text: str = Field(..., description="The updated content of the comment")
