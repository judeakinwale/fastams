from fastapi import FastAPI, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mongo_db import db
from starlette.responses import FileResponse, HTMLResponse

# from sqlite_database import engine # for sqlite db
# from database import engine # for postgres db
import models, user, location, attendance, auth, settings
from mongo_db import client, db

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
client
db

# from fastapi.security import HTTPBearer
# security = HTTPBearer()


# origins = ["http://localhost:3000", "http://localhost:5000"] # to test cors works
# origins = ["http://localhost:3000", "https://localhost:3000"] # for production

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins, # for production
    allow_origins=["*"],  # for development
    # # allow_origins cannot be set to ['*'] for credentials to be allowed, origins must be specified
    # allow_credentials=True, # Indicate that cookies should be supported for cross-origin requests. Defaults to False
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["Auth"], prefix="/api/v1/auth")
app.include_router(user.router, tags=["User"], prefix="/api/v1/user")
app.include_router(location.router, tags=["Location"], prefix="/api/v1/location")
app.include_router(attendance.router, tags=["Attendance"], prefix="/api/v1/attendance")
app.include_router(settings.router, tags=["Settings"], prefix="/api/v1/settings")


# mount static folders
# app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.mount("/static", StaticFiles(directory="static/static"), name="static")
app.mount(
    "/attendance_images",
    StaticFiles(directory="attendance_images"),
    name="attendance_images",
)
app.mount(
    "/attendance_qr_codes",
    StaticFiles(directory="attendance_qr_codes"),
    name="attendance_qr_codes",
)
app.mount("/qr_codes", StaticFiles(directory="qr_codes"), name="qr_codes")
app.mount(
    "/training_images", StaticFiles(directory="training_images"), name="training_images"
)


# static frontend
# Render index.html
@app.get("/")
async def index():
    return FileResponse("./static/index.html")
    # return HTMLResponse("static/index.html")


# Render index.html
# Handle for extra url paths in index.html and page reloads
@app.get("/{full_path:path}/")
async def root(full_path: str | None = None):
    return FileResponse("./static/index.html")
    # return HTMLResponse("static/index.html")


# # Render index.html
# @app.get("/")
# async def read_index():
#     return FileResponse("./static/index.html")


# @app.get("/.*", include_in_schema=False)
# def root():
#     return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


# @app.get("/")
# async def root():
#     return {"message": "Welcome to the attendance management system"}
