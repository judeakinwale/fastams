from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from sqlite_database import engine # for sqlite db
# from database import engine # for postgres db
import models, user, location, attendance

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(user.router, tags=['User'], prefix='/api/v1/user')
app.include_router(location.router, tags=['Location'], prefix='/api/v1/location')
app.include_router(attendance.router, tags=['Location'], prefix='/api/v1/attendance')


@app.get("/")
async def root():
  return {"message": "Welcome to the attendance management system"}
