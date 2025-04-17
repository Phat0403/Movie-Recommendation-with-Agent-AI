from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.auth import router as auth_router

from db.session import engine
from models.user import User

# Create the database tables if they don't exist
User.metadata.create_all(bind=engine)

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
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI User Management API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)