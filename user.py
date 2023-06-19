from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
import models
import schemas
import utils
import json

router = APIRouter()


def get_detailed_user(user):
  user = utils.mongo_res(user)

  attendance_history = [utils.mongo_res(attendance) for attendance in models.AttendanceHistory.find({'email': user['email']})]
  user['attendance_history'] = attendance_history

  location = utils.mongo_res(models.Location.find_one({'_id': user['location_id']}))
  user['location'] = location

  return user


def update_payload_with_password_hash(payload: schemas.CreateUser) -> schemas.CreateUser:
  password = payload.pop("password")
  if password:
    print(payload)
    payload["hashed_password"] = utils.get_password_hash(password)

  return payload


def save_user_image_file(first_name: str, email: str, file: UploadFile | None = File(None)) -> str:
  # generate unique name for image
  random_chars = utils.random_string(5) # for generating random strings for image and qr code
  file_extension = utils.get_file_extension(file.filename)
  relative_image_path = f"./training_images/{first_name}-{email}-{random_chars}{file_extension}"

  # save file to training images folder
  with open(relative_image_path, "wb") as buffer:
    # print(buffer)
    copyfileobj(file.file, buffer)

  return relative_image_path


def generate_base_64_image(image_path) -> str:
  import base64
  # Convert the image to base64 format
  with open(image_path, "rb") as f:
    encoded_image = base64.b64encode(f.read())

  return encoded_image


def send_account_creation_email(email: str, first_name: str, image_path: str):
  reciepients = [email]
  subject = f"Attendance QR Code"
  message = f"""
  <p>Hello {first_name},</p>
  <br>
  <p>Kindly find your attendance QR Code attached.</p>
  """
  image_path = image_path
  image_name = "QR Code"
  result = utils.send_email(reciepients, subject, message, image_path, image_name)
  print("email result: ", result, type(result))

  return result


# [...] generic function for creating users
def user_factory(payload: schemas.CreateUser, file: UploadFile | None = File(None)) -> schemas.UserResponse:
  print({"payload": payload})

  email = payload['email']
  first_name = payload['first_name']

  if not utils.validate_email(email):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email Provided")

  db_user = utils.mongo_res(models.User.find_one({'email': email}))
  if db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

  payload = update_payload_with_password_hash(payload)

  relative_image_path = None
  if file:
    print({'file': file})
    relative_image_path = save_user_image_file(first_name, email, file)

    # get image and face encodings from uploaded file
    image_encoding, face_encoding = utils.check_face_in_picture(file.file)
    # image_encoding_str = json.dumps(image_encoding.tolist())
    image_encoding_str = json.dumps([]) # Image encoding is not needed
    face_encoding_str = json.dumps(face_encoding.tolist())

    # update user instance with image and encodings
    payload.update({"image": relative_image_path, "image_encoding": image_encoding_str, "face_encoding": face_encoding_str})

  # generate a qr code
  random_chars = utils.random_string(5)
  user_qr_code = utils.generate_qr_code(email, f"./qr_codes/{email}-{random_chars}")

  # generate b64 image of the qr code for display
  encoded_image = generate_base_64_image(user_qr_code)
    
  # update payload
  payload.update({"qr_code": user_qr_code, "qr_code_content": email, "qr_code_b64": encoded_image})
  print({'payload before create': payload})

  created_id = models.User.insert_one(payload).inserted_id
  user = get_detailed_user(models.User.find_one({'_id': created_id}))

  send_account_creation_email(email, first_name, user_qr_code)

  return {"status": "success", "data": user, "b64_qr_code": encoded_image}


# [...] get all users
@router.get('/', response_model=schemas.ListUserResponse)
# @router.get('/')
def get_users(limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  users = [get_detailed_user(user) for user in models.User.find()]

  return {'status': 'success', 'count': len(users), 'data': users}


# [...] create user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(
  first_name: str = Form(...), 
  last_name: str = Form(...),
  email: str = Form(...),
  location_id: str | None = Form(None),
  file: UploadFile | None = File(None), 
):
  payload = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "location_id": location_id,
    # "password": password,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
  }
  print({"payload_dict": payload})

  return user_factory(payload, file)


# [...] create admin user
@router.post('/admin', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse, summary="Create Admin User")
def create_admin_user(
  first_name: str = Form(...), 
  last_name: str = Form(...),
  email: str = Form(...),
  password: str = Form(...),
  location_id: str | None = Form(None),
  file: UploadFile | None = File(None), 
  current_user: models.User = Depends(utils.get_current_active_user),
):
  payload = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "location_id": location_id,
    "password": password,
    "is_admin": True,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
  }
  print({"payload_dict": payload})

  return user_factory(payload, file)


# [...] get user by id
@router.get('/{user_id}', response_model=schemas.UserResponse)
def get_user(user_id: str):
  user = get_detailed_user(models.User.find_one({'_id': ObjectId(user_id)}))
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  return {"status": "success", "data": user}


# [...] edit user by id
@router.patch('/{user_id}', response_model=schemas.UserResponse)
def update_user(user_id: str, payload: schemas.UpdateUser):
  existingUser = utils.mongo_res(models.User.find_one({'_id': ObjectId(user_id)}))
  if not existingUser:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  payload = payload.dict(exclude_unset=True)
  payload = update_payload_with_password_hash(payload)
  payload.update({'updated_at': datetime.now()})
  print({"payload": payload})

  user = get_detailed_user(models.User.find_one_and_update({'_id': ObjectId(user_id)}, {'$set': payload}, return_document=ReturnDocument.AFTER))
  return {"status": "success", "data": user}


# [...] update user photo by user id
@router.patch('/{user_id}/image', response_model=schemas.UserResponse)
def update_user(user_id: str, file: UploadFile = File(...)):
  existingUser = utils.mongo_res(models.User.find_one({'_id': ObjectId(user_id)}))
  if not existingUser:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  relative_image_path = save_user_image_file(existingUser['first_name'], existingUser['email'])

  # get image and face encodings from uploaded file
  image_encoding, face_encoding = utils.check_face_in_picture(file.file)
  # image_encoding_str = json.dumps(image_encoding.tolist())
  image_encoding_str = json.dumps([]) # Image encoding is not needed
  face_encoding_str = json.dumps(face_encoding.tolist())

  print(relative_image_path, image_encoding, face_encoding)

  # update user instance with image and encodings
  payload = {
    "image": relative_image_path, 
    "image_encoding": image_encoding_str, 
    "face_encoding": face_encoding_str,
    "updated_at": datetime.now(),
  }  
  user = get_detailed_user(models.User.find_one_and_update({'_id': ObjectId(user_id)}, {'$set': payload}, return_document=ReturnDocument.AFTER))

  return {"status": "success", "data": user}


# [...] delete user by id
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
  user = utils.mongo_res(models.User.find_one_and_delete({'_id': ObjectId(user_id)}))
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  return Response(status_code=status.HTTP_204_NO_CONTENT)
