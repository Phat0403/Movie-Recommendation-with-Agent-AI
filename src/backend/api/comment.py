from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import logging

from db.clients import get_db
from services.comment import CommentService
from core.api import get_user_from_request
from schemas.comment import CommentList, Comment, CommentCreate, CommentUpdate
from sqlalchemy.orm import Session

router = APIRouter()

def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(db=db)

@router.get("/comment/{comment_id}", response_model=Comment)
async def get_comment(comment_id: int, comment_service: CommentService = Depends(get_comment_service)):
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
async def get_comments_by_movie_id(movie_id: str, comment_service: CommentService = Depends(get_comment_service)):
    if not movie_id:
        raise HTTPException(status_code=400, detail="Movie ID is required")
    try:
        comments = comment_service.get_comments_by_movie_id(movie_id)
        return comments
    except Exception as e:
        logging.error(f"Error fetching comments for movie {movie_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/comments/user/{username}", response_model=CommentList)
async def get_comment_by_username(username: str, request: Request, comment_service: CommentService = Depends(get_comment_service)):
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    if user.get("username") != username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")
    try:
        comments = comment_service.get_comments_by_username(username)
        if comments is None:
            raise HTTPException(status_code=404, detail="No comments found")
        return comments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/comment")
async def create_comment(payload: CommentCreate, request: Request, comment_service: CommentService = Depends(get_comment_service)):
    if not payload.movie_id or not isinstance(payload.movie_id, str):
        raise HTTPException(status_code=400, detail="Movie ID must be a string")
    if not payload.comment_text:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    username = user.get("username")
    if not username:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    try:
        result = comment_service.create(payload.movie_id, username, payload.comment_text)
        return JSONResponse(content={"comment": result.as_dict(), "message": "Comment created successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/comment/{comment_id}")
async def delete_comment(comment_id: int, request: Request, comment_service: CommentService = Depends(get_comment_service)):
    if not comment_id or not isinstance(comment_id, int):
        raise HTTPException(status_code=400, detail="Valid Comment ID is required")

    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")

    comment_info = comment_service.get(comment_id)
    if not comment_info:
        raise HTTPException(status_code=404, detail="Comment not found")
    if user.get("username") != comment_info.username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        comment_service.delete(comment_id)
        return JSONResponse(content={"message": f"Comment {comment_id} deleted successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/comment")
async def update_comment(payload: CommentUpdate, request: Request, comment_service: CommentService = Depends(get_comment_service)):
    if not payload.comment_id or not isinstance(payload.comment_id, int):
        raise HTTPException(status_code=400, detail="Valid Comment ID is required")
    if not payload.comment_text:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")

    comment_info = comment_service.get(payload.comment_id)
    if not comment_info:
        raise HTTPException(status_code=404, detail="Comment not found")
    if user.get("username") != comment_info.username and not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not authorized")

    try:
        updated_comment = comment_service.update(payload.comment_id, payload.comment_text)
        return JSONResponse(content={"comment": updated_comment.as_dict(), "message": "Comment updated successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
