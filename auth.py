from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
from datetime import datetime, timedelta
import models
import schemas
import utils

router = APIRouter()


# [...] authenticate user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def login(payload: schemas.UserLogin):
  payload = payload.dict(exclude_unset=True)
  email = payload['email']
  password = payload['password']

  user = utils.authenticate_user(email, password)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  
  token = utils.create_access_token(user)
  return {"status": "success", "data": user, "token": token}


# [...] authenticate user using OAuth2
# @router.post('/token', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/token', status_code=status.HTTP_201_CREATED)
def login(username: str = Form(...), password: str = Form(...)):
  email = username

  user = utils.authenticate_user(email, password)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid username or password")
  
  token = utils.create_access_token(user)
  return {
    "status": "success", "data": user, "token": token, 
    "access_token": token, "token_type": "bearer" # For OAuth2
  }


# [...] get authenticated user
# @router.get('/me')
@router.get('/me', response_model=schemas.UserResponse)
def get_auth_user(current_user: models.User = Depends(utils.get_current_active_user)):
  user = current_user
  return {"status": "success", "data": user}


# [...] get authenticated user using OAuth2
# @router.get('/me/oauth')
@router.get('/me/oauth', response_model=schemas.UserResponse)
def get_oauth2_user(current_user: models.User = Depends(utils.get_current_oauth2_user)):
  user = current_user
  return {"status": "success", "data": user}


# [...] forgot password
@router.get('/forgot-password', response_model=schemas.ResetPasswordResponse)
def forgot_password(email: str):
  user = utils.mongo_res(models.User.find_one({"email": email}))

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found') # change the message

  payload = {
    'reset_password_token': utils.generate_unique_token(),
    'reset_token_expire': datetime.now() + timedelta(hours=1),
    'updated_at': datetime.now(),
  }  
  user = utils.mongo_res(models.User.find_one_and_update({'_id': ObjectId(user["id"])}, {'$set': payload}, return_document=ReturnDocument.AFTER))

  url = "https://pyams.azurewebsites.net/"
  reciepients = [email]
  subject = f"Forgot Password"
  message = f"""
  <p>Hello {user.first_name},</p>
  <br>
  <p>You have requested to reset your password. If you didn't make this request kindly ignore.</p>
  <p>Kindly reset your password at this <a href='{url}'>link</a>.</p>"""
  utils.send_email(reciepients, subject, message)

  # TODO: send email to user with link to reset password
  return {"status": "success", "data": user}


# [...] reset password
@router.post('/reset-password/{reset_token}', response_model=schemas.ResetPasswordResponse)
def reset_password(reset_token: str, payload: schemas.ResetPassword):
  user = utils.mongo_res(models.User.find({"reset_password_token": reset_token, "reset_token_expire": {"$lte": datetime.now()}}))

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid password reset request.')

  payload = payload.dict(exclude_unset=True)
  payload['reset_password_token'] = None
  payload['reset_token_expire'] = None
  payload['updated_at'] = datetime.now()

  if "password" in payload:
    password = payload.pop("password")
    payload["hashed_password"] = utils.get_password_hash(password)

  user = utils.mongo_res(models.User.find_one_and_update({'_id': ObjectId(user["id"])}, {'$set': payload}, return_document=ReturnDocument.AFTER))

  return {"status": "success", "data": user}
