from fastapi import APIRouter, HTTPException, Request, Depends, Body
from fastapi.responses import JSONResponse

from core.api import get_user_from_request
from db.clients import get_db
from services.user import UserService

def get_user_service(db=Depends(get_db)) -> UserService:
    return UserService(db=db)

router = APIRouter()
@router.get("/user-info")
async def get_user(user_service: UserService = Depends(get_user_service), request: Request = None):
    """
    Get user information by username.
    """
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    username = user.get("username")
    try:
        user_info = user_service.get_user_info(username)
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
        return JSONResponse(content=user_info, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/user-favorites")
async def get_user_favorites(user_service: UserService = Depends(get_user_service), request: Request = None):
    """
    Get user favorites by username.
    """
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    username = user.get("username")
    try:
        favorites = user_service.get_favorite_movies(username)
        return JSONResponse(content=favorites, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/add-favorite")
async def add_favorite(
    movie_id: str = Body(..., embed=True, description="Movie ID to be added as favorite"),
    user_service: UserService = Depends(get_user_service),
    request: Request = None
):
    """
    Add a movie to the user's favorite list.
    """ 
    print(f"Adding favorite movie: {movie_id}")
    import logging
    logging.error(f"Adding favorite movie: {movie_id}")
    response = await get_user_from_request(request)
    print(f"Response from get_user_from_request: {response}")
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    username = user.get("username")
    try:
        result = user_service.add_favorite_movie(username, movie_id)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to add favorite movie")
        return JSONResponse(content={"message": "Movie added to favorites successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/remove-favorite")
async def remove_favorite(
    movie_id: str = Body(..., embed=True, description="Movie ID to be removed from favorites"),
    user_service: UserService = Depends(get_user_service),
    request: Request = None
):
    """
    Remove a movie from the user's favorite list.
    """
    
    response = await get_user_from_request(request)
    if response.get("status_code") != 200:
        raise HTTPException(status_code=response.get("status_code"), detail=response.get("message"))
    user = response.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User is not authenticated")
    
    username = user.get("username")
    try:
        result = user_service.remove_favorite_movie(username, movie_id)
        if not result:
            raise HTTPException(status_code=400, detail="Failed to remove favorite movie")
        return JSONResponse(content={"message": "Movie removed from favorites successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
