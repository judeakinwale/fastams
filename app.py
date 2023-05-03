from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from sqlite_database import engine # for sqlite db
# from database import engine # for postgres db
import models, user, location, attendance, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = ["http://localhost:3000"] # to test cors works
# origins = ["http://localhost:3000", "https://localhost:3000"] # for production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # for production
    # allow_origins=["*"], # for development
    # allow_credentials=True, # Indicate that cookies should be supported for cross-origin requests. Defaults to False 
    # # allow_origins cannot be set to ['*'] for credentials to be allowed, origins must be specified
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth.router, tags=['Auth'], prefix='/api/v1/auth')
app.include_router(user.router, tags=['User'], prefix='/api/v1/user')
app.include_router(location.router, tags=['Location'], prefix='/api/v1/location')
app.include_router(attendance.router, tags=['Attendance'], prefix='/api/v1/attendance')


@app.get("/")
async def root():
  return {"message": "Welcome to the attendance management system"}
