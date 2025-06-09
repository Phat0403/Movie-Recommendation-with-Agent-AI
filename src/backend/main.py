from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.movie import router as movie_router
from api.comment import router as comment_router
from api.user import router as user_router
from api.chatbot import router as chatbot_router
from db.session import engine, Base

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(

    title="FastAPI User Management",
    description="A simple user management system using FastAPI.",
    version="1.0.0",
)

# Middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the user router
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(movie_router, prefix="/api", tags=["movies"])
app.include_router(comment_router, prefix="/api", tags=["comments"])
app.include_router(user_router, prefix="/api/user", tags=["user"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["chatbot"])


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI User Management API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)