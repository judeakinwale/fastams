import os
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter, Response, Request, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from bson.objectid import ObjectId
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


def get_app_settings():
  settings = mongo_res(models.Settings.find_one())
  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Settings not found. Setup the site settings first!')
  return settings


def is_location_used() -> bool:
  print("get_app_settings():", get_app_settings())
  return get_app_settings()["use_location"]


def is_facial_recognition_used() -> bool:
  print("get_app_settings():", get_app_settings())
  return get_app_settings()["use_facial_recognition"]


def is_qr_code_used() -> bool:
  print("get_app_settings():", get_app_settings())
  return get_app_settings()["use_qr_code"]



# auth utils
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
  return password_context.hash(password)


def verify_password(plain_password, hashed_password):
  return password_context.verify(plain_password, hashed_password)


def get_user_by_email(email: str):
  return mongo_res(models.User.find_one({'email': email}))
  

def authenticate_user(email: str, password: str):
  user = get_user_by_email(email)
  if not user:
    return False
  if not verify_password(password, user["hashed_password"]):
    return False
  return user

# //Generate and hash password token
# User.methods.getResetPasswordToken = function () {
#   //Generate token
#   const resetToken = crypto.randomBytes(20).toString("hex");
#   //Hash token and set to resetPasswordToken field
#   this.resetPasswordToken = crypto
#     .createHash("sha256")
#     .update(resetToken)
#     .digest("hex");

#   //set expire
#   this.resetPasswordExpire = Date.now() + 10 * 60 * 1000;
#   return resetToken;
# };

def generate_unique_token():
  # if not string: string = random_string(32)
  import uuid
  return uuid.uuid4().hex



jwt_settings = JWTSettings()

def create_access_token(user: User):
    # expires_delta = timedelta(minutes=jwt_settings.access_token_expire_minutes)
    expires_delta = timedelta(days=jwt_settings.access_token_expire)
    to_encode = {"id": str(user["id"]), "exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")
security = HTTPBearer()


def decode_token_id(request: Request):
  auth = request.headers.get("Authentication")
  token = auth.split(" ")[1]
  print({"auth": auth, "token": token})
  payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
  print({"token": token, "payload": payload})
  user_id = payload.get("id")
  if user_id is None:
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
  # token_data = TokenData(user_id=user_id)


def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
  try:      
    token = credentials.credentials
    payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
    print({"token": token, "payload": payload})
    user_id = payload.get("id")
    if user_id is None:
      raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # token_data = TokenData(user_id=user_id)
  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid authentication credentials")
  except AttributeError:
    # if credentials.credentials doesnt exist
    raise HTTPException(status_code=401, detail="Invalid authentication credentials...")

  user = mongo_res(models.User.find_one({"_id": ObjectId(user_id)}))
  if user is None:
    raise HTTPException(status_code=404, detail="User not found")
  return user


def try_get_current_active_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
  print(credentials.credentials)
  try:      
    token = credentials.credentials
    payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
    print({"token": token, "payload": payload})
    user_id = payload.get("id")
    if user_id is None:
      return None
    # token_data = TokenData(user_id=user_id)
  except JWTError:
    return None
  except AttributeError:
    # if credentials.credentials doesnt exist
    return None

  user = mongo_res(models.User.find_one({"_id": user_id}))
  if user is None:
    return None
  return user


# def get_current_oauth2_user(token: str = Depends(oauth2_scheme)):
def get_current_oauth2_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        print({"token": token, "oauth2_scheme": oauth2_scheme})
        payload = jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
        user_id = payload.get("id")
        print({"user_id": user_id, "payload": payload})

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        # token_data = TokenData(user_id=user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = mongo_res(models.User.find_one({"_id": user_id}))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print({"user": user})

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


# def send_email():
#   import smtplib, ssl

#   # port = 465  # For SSL
#   username = os.environ('SMTP_EMAIL') or 'Bizsupport@lotusbetaanalytics.com'
#   password = os.environ('SMTP_PASSWORD')
#   host = os.environ('SMTP_HOST') or 'smtp.office365.com'
#   port = os.environ('SMTP_PORT') or 587

#   # password = input("Type your password and press enter: ")

#   # Create a secure SSL context
#   context = ssl.create_default_context()

#   with smtplib.SMTP_SSL(host, port, context=context) as server:
#       server.login(username, password)
#       # TODO: Send email here


def send_email(reciepients, subject, message, image_path = None, image_name = '', cc = []):
  import smtplib
  from email.mime.text import MIMEText
  from email.mime.image import MIMEImage
  from email.mime.multipart import MIMEMultipart
  
  email = os.environ['SMTP_EMAIL'] or 'Bizsupport@lotusbetaanalytics.com'
  password = os.environ['SMTP_PASSWORD']
  host = os.environ['SMTP_HOST'] or 'smtp.office365.com'
  port = os.environ['SMTP_PORT'] or 587

  # Create a MIME multipart message
  msg = MIMEMultipart()
  msg['From'] = email
  msg['To'] = ', '.join(reciepients)
  msg['Cc'] = ', '.join(cc)
  msg['Subject'] = subject

  # Attach the message to the MIME message
  msg.attach(MIMEText(message, 'html'))
  # msg.attach(MIMEText(message, 'plain'))

  # Attach the image
  if image_path:
    with open(image_path, 'rb') as f:
      img_data = f.read()
      image = MIMEImage(img_data, name=f'{image_name if image_name else "image"}.png')
      msg.attach(image)

  # Connect to the SMTP server 
  server = smtplib.SMTP(host, port)
  server.starttls()

  # Login to your account
  server.login(email, password)

  all_reciepients = reciepients + cc

  # Send the email
  response = server.sendmail(email, all_reciepients, msg.as_string())

  # Close the connection
  server.quit()

  return response



# # Provide the necessary information
# email = 'your_email@gmail.com'
# password = 'your_password'
# reciepients = 'recipient_email@example.com'
# subject = 'Hello from Python!'
# message = 'This is a test email sent using Python.'

# # Call the function to send the email
# send_email(email, password, reciepients, subject, message)


# def send_mail(options):
#   import smtplib

#   message = """From: From Person <from@fromdomain.com>
#   To: To Person <to@todomain.com>
#   MIME-Version: 1.0
#   Content-type: text/html
#   Subject: SMTP HTML e-mail test

#   This is an e-mail message to be sent in HTML format

#   <b>This is HTML message.</b>
#   <h1>This is headline.</h1>
#   """

#   try:
#     smtpObj = smtplib.SMTP('localhost')
#     smtpObj.sendmail(sender, receivers, message)         
#     print("Successfully sent email")
#   except SMTPException:
#     print("Error: unable to send email")


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
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'No face found in uploaded image')


def check_face_match(user_face_encoding, attendance_face_encoding):
  # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
  matches = face_recognition.compare_faces([user_face_encoding], attendance_face_encoding)
  if True in matches:
    return True
  return False
# facial recognition utils


# location utils
def check_matching_location(location, long, lat, rad = 0.0005):
  if not (location.longitude and location.latitude): return True

  long_diff = abs(float(location.longitude) - float(long))
  lat_diff = abs(float(location.latitude) - float(lat))
  location_rad = float(location.radius) if location.radius else rad

  if long_diff < rad and lat_diff < location_rad:
    return True
  return False
# location utils


# fix response from mongo db before display
def mongo_res(instance):
  if not instance: return

  str_id = str(instance['_id'])
  instance['id'] = str_id
  instance['_id'] = str_id
  # print({"instance": instance})
  return instance
