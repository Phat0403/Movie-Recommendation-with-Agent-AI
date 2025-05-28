from fastapi import Request
import httpx
import logging
async def get_user_from_request(request: Request):
    """
    Extract the user from the request object.
    
    Args:
        request (Request): The FastAPI request object.
    
    Returns:
        dict: A dictionary containing user information.
    """
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return {"status_code": 401, "message": "Authorization header is missing"}
    if not authorization_header.startswith("Bearer "):
        return {"status_code": 401, "message": "Invalid authorization header format"}
    token = authorization_header.split(" ")[1]
    if not token:
        return {"status_code": 401, "message": "Token is required"}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/auth/me", headers={"Authorization": authorization_header})
        if response.status_code != 200:
            return {"status_code": response.status_code, "message": "Failed to fetch user information"}
        user_info = response.json()
        return {"status_code": 200, "message": "User information retrieved successfully", "user": user_info}
    except httpx.RequestError as e:
        return {"status_code": 500, "message": f"Request error: {str(e)}"}