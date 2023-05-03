from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
import models
import schemas
import utils

router = APIRouter()


# [...] authenticate user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
  login_details = payload.dict()
  email = login_details['email']
  password = login_details['password']
  user = utils.authenticate_user(email, password, db)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  token = utils.create_access_token(user)
  return {"status": "success", "data": user, "token": token}
# def login(email: str, password: str, db: Session = Depends(get_db)):
#   user = utils.authenticate_user(email, password, db)
#   if not user:
#     raise HTTPException(status_code=401, detail="Invalid email or password")
#   token = utils.create_access_token(user)
#   return {"status": "success", "data": user, "token": token}


# [...] get authenticated user
# @router.get('/me', response_model=schemas.User)
@router.get('/me')
def get_auth_user(current_user: models.User = Depends(utils.get_current_active_user)):
  user = current_user
  return {"status": "success", "data": user}