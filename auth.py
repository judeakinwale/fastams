from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
from datetime import datetime, timedelta
import models
import schemas
import utils

router = APIRouter()


# [...] authenticate user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
  login_details = payload.dict(exclude_unset=True)
  email = login_details['email']
  password = login_details['password']

  user = utils.authenticate_user(email, password, db)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  
  token = utils.create_access_token(user)
  return {"status": "success", "data": user, "token": token}


# [...] get authenticated user
# @router.get('/me')
@router.get('/me', response_model=schemas.User)
def get_auth_user(current_user: models.User = Depends(utils.get_current_active_user)):
  user = current_user
  return {"status": "success", "data": user}


# [...] forgot password
@router.get('/forgot-password', response_model=schemas.ResetPasswordResponse)
def forgot_password(email: str, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.email == email)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found') # change the message

  update_data = {
    'reset_password_token': utils.generate_unique_token(),
    'reset_token_expire': datetime.now() + timedelta(hours=1),
  }

  get_user.filter(models.User.email == email).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)

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
def reset_password(reset_token: str, payload: schemas.ResetPassword, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(
    models.User.reset_password_token == reset_token, 
    models.User.reset_token_expire <= datetime.now()
  )
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid password reset request.')

  update_data = payload.dict(exclude_unset=True)
  update_data['reset_password_token'] = None
  update_data['reset_token_expire'] = None

  if "password" in update_data:
    password = update_data.pop("password")
    print(update_data)
    update_data = {**update_data, "hashed_password": utils.get_password_hash(password)}

  get_user.filter(models.User.reset_password_token == reset_token).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)

  return {"status": "success", "data": user}
