import os
from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
import face_recognition
import cv2
import numpy as np
from PIL import Image
from passlib.context import CryptContext
import models
from datetime import datetime, timedelta
from jose import JWTError, jwt
from models import User
from config import JWTSettings

# auth utils
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
  return password_context.hash(password)


def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)


def get_user_by_email(email: str, db: Session = Depends(get_db)):
  return db.query(models.User).filter(models.User.email == email).first()
  

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
  user = get_user_by_email(email, db)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user


jwt_settings = JWTSettings()

def create_access_token(user: User):
    # expires_delta = timedelta(minutes=jwt_settings.access_token_expire_minutes)
    expires_delta = timedelta(days=jwt_settings.access_token_expire)
    to_encode = {"id": str(user.id), "exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_active_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        # token_data = TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(models.User).filter(models.User.id == user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# auth utils


def random_string(num: int) -> str:
  import string
  import random

  # using random.choices() to generate random strings
  res = ''.join(random.choices(string.ascii_letters + string.digits, k=num))
  return res


def get_file_extension(filePath: str) -> str:
  file_name, file_extension = os.path.splitext(filePath)
  print(file_name, file_extension)
  return file_extension


def validate_email(email: str) -> bool:
  import re
 
  # Make a regular expression for validating email
  regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

  if(re.fullmatch(regex, email)):
    return True
  return False


def get_opencv_img_from_buffer(buffer, flags = None):
  bytes_as_np_array = np.frombuffer(buffer.read(), dtype=np.uint8)
  return cv2.imdecode(bytes_as_np_array, flags)


# qr code utils
def generate_qr_code(data_str: str, file_path: str) -> str:
  import qrcode
  img = qrcode.make(data_str)
  type(img)  # qrcode.image.pil.PilImage
  full_path = f"{file_path}-qr.png"
  img.save(full_path)
  return full_path


def read_qr_code(file_path: str , is_opencv_img = False) -> str | None:
  try:
    print(file_path)
    img = file_path
    if not is_opencv_img:
      img = cv2.imread(file_path)

    detect = cv2.QRCodeDetector()
    value, points, straight_qrcode = detect.detectAndDecode(img)
    return value
  except Exception() as e:
    print(f"Error reading qr code content, {e}")
    return
# qr code utils


# facial recognition utils
def check_face_in_picture(imagePath: str):
  try:
    # TODO: reduce frame size and image resolution
    image_encoding = face_recognition.load_image_file(imagePath)
    face_encoding = face_recognition.face_encodings(image_encoding)[0]
    return image_encoding, face_encoding
  except:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST400, detail=f'No face found in uploaded image')


def check_face_match(user_face_encoding, attendance_face_encoding):
  # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
  matches = face_recognition.compare_faces([user_face_encoding], attendance_face_encoding)
  if True in matches:
    return True
  return False
# facial recognition utils
