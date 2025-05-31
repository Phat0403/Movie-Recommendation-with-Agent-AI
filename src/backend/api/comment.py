from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import logging

from db.clients import get_db
from services.comment import CommentService
from core.api import get_user_from_request
from schemas.comment import CommentList, Comment, CommentCreate, CommentUpdate

# Initialize the CommentService instance using the correct db dependency
db = next(get_db())  # Fetch the database connection
comment_service = CommentService(db=db)

router = APIRouter()

@router.get("/comment/{comment_id}", response_model=Comment)
async def get_comment(comment_id: int):
    """
    Get a comment by its ID.
    """
    if not comment_id or not isinstance(comment_id, int):
        raise HTTPException(status_code=400, detail="Valid Comment ID is required")
    try:
        comment = comment_service.get(comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comments/movie/{movie_id}", response_model=CommentList)
async def get_comments_by_movie_id(movie_id: str):
    """
    Get all comments for a specific movie.
    """
    if not movie_id:
        raise HTTPException(status_code=400, detail="Movie ID is required")
    try:
        comments = comment_service.get_comments_by_movie_id(movie_id)
        return comments
    except Exception as e:
        logging.error(f"Error fetching comments for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/comments/user/{username}", response_model=CommentList)
async def get_comment_by_username(username: str, request: Request = None):
    """
    Get all comments made by a specific user.
    """
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.status_code, detail=response.get("message", "Failed to fetch user information"))
    user = response.get("user")
    logging.warning(f"User from request: {user}")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    if user.get("username") != username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="You are not authorized to view this user's comments")
    try:
        comments = comment_service.get_comments_by_username(username)
        if comments is None:
            raise HTTPException(status_code=404, detail="No comments found for this user")
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/comment")
async def create_comment(payload: CommentCreate, request: Request = None):
    """
    Create a new comment for a movie.
    """
    movie_id = payload.movie_id
    comment_text = payload.comment_text
    if not movie_id:
        raise HTTPException(status_code=400, detail="Movie ID is required")
    if not isinstance(movie_id, str):
        raise HTTPException(status_code=400, detail="Movie ID must be a string")
    if not comment_text:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")

    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message", "Failed to fetch user information"))
    user = response.get("user")
    username = user.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="User is not authenticated")

    try:
        response = comment_service.create(movie_id, username, comment_text)
        return JSONResponse(content={"comment": response.as_dict(), "message": "Comment created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/comment/{comment_id}", response_model=dict)
async def delete_comment(comment_id: int, request: Request = None):
    """
    Delete a comment by its ID.
    """
    if not comment_id or not isinstance(comment_id, int):
        raise HTTPException(status_code=400, detail="Valid Comment ID is required")
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.status_code, detail=response.get("message", "Failed to fetch user information"))
    
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    
    comment_info = comment_service.get(comment_id)
    logging.warning(f"Comment info for deletion: {comment_info}")
    if not comment_info:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if user.get("username") != comment_info.username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="You are not authorized to delete this comment")
    try:
        comment_service.delete(comment_id)
        return JSONResponse(content={"message": f"Comment with id {comment_id} deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/comment")
async def update_comment(payload: CommentUpdate, request: Request = None):
    """
    Update a comment by its ID.
    """
    comment_id = payload.comment_id
    comment_text = payload.comment_text
    if not comment_id or not isinstance(comment_id, int):
        raise HTTPException(status_code=400, detail="Valid Comment ID is required")
    if not comment_text:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.status_code, detail=response.get("message", "Failed to fetch user information"))
    user = response.get("user")

    comment_info = comment_service.get(comment_id)

    if not comment_info:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if user.get("username") != comment_info.username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="You are not authorized to update this comment")
    
    try:
        updated_comment = comment_service.update(comment_id, comment_text)
        if not updated_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return JSONResponse(content={"comment": updated_comment.as_dict(), "message": "Comment updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
