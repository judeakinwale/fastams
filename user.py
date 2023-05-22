from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
import models
import schemas
import utils
import json

router = APIRouter()


# [...] get all users
@router.get('/', response_model=schemas.ListUserResponse)
# @router.get('/')
def get_users(db: Session = Depends(get_db), limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  users = db.query(models.User).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(users), 'data': users}


# [...] create user
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(
  first_name: str = Form(...), 
  last_name: str = Form(...),
  email: str = Form(...),
  password: str | None = Form(None),
  location_id: str | None = Form(None),
  is_admin: str | None = Form(None),
  file: UploadFile | None = File(None), 
  db: Session = Depends(get_db),
  # current_user: models.User | None = Depends(utils.get_current_active_user) or None,
  current_user: models.User | None = Depends(utils.try_get_current_active_user),
  # _ = Depends(utils.security),
):
# def create_user(payload: schemas.CreateUser = Depends(), file: UploadFile | None = None, db: Session = Depends(get_db)):
# def create_user(payload: schemas.CreateUser, file: UploadFile | None = File(...), db: Session = Depends(get_db)):
  payload_dict = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "location_id": location_id,
    "password": password,
  } # convert payload to dictionary
  print({"payload.dict": payload_dict})
  # payload_dict = payload.dict() # convert payload to dictionary
  # print({"payload": payload, "payload.dict": payload_dict})
  updated_payload = payload_dict

  if not utils.validate_email(email):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email Provided")

  db_user = utils.get_user_by_email(payload_dict["email"], db)
  if db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

  if not current_user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorized to create admin")

  # if is_admin:
  #   try: 
  #     current_user = utils.get_current_active_user(utils.security, db)
  #     print({"current_user": current_user})
  #   except HTTPException as e: 
  #     # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You're not authorized to create admin")
  #     raise e
      
  # if payload_dict["password"]:
  # if "password" in payload_dict:
  if password:
    password = payload_dict.pop("password")
    print(payload_dict)
    updated_payload = {**payload_dict, "hashed_password": utils.get_password_hash(password)}
  else: payload_dict.pop("password")

  random_chars = utils.random_string(5) # for generating random strings for image and qr code
  relative_image_path = None
  if file:
    # generate unique name for image
    file_extension = utils.get_file_extension(file.filename)
    relative_image_path = f"./training_images/{first_name}-{email}-{random_chars}{file_extension}"

    # save file to training images folder
    with open(relative_image_path, "wb") as buffer:
      # print(buffer)
      copyfileobj(file.file, buffer)

    # get image and face encodings from uploaded file
    image_encoding, face_encoding = utils.check_face_in_picture(file.file)
    # image_encoding_str = json.dumps(image_encoding.tolist())
    image_encoding_str = json.dumps([]) # Image encoding is not needed
    face_encoding_str = json.dumps(face_encoding.tolist())

    print(relative_image_path)
    # print(relative_image_path, image_encoding, face_encoding)

    # update user instance with image and encodings
    updated_payload = {**updated_payload, "image": relative_image_path, "image_encoding": image_encoding_str, "face_encoding": face_encoding_str}  

  # generate a qr code
  user_email = updated_payload["email"]
  user_qr_code = utils.generate_qr_code(user_email, f"./qr_codes/{user_email}-{random_chars}")

  # generate b64 image of the qr code for display
  encoded_image = None
  if user_qr_code:
    import base64
    # Convert the image to base64 format
    with open(user_qr_code, "rb") as f:
      encoded_image = base64.b64encode(f.read())

  updated_payload["qr_code"] = user_qr_code
  updated_payload["qr_code_content"] = user_email
  updated_payload["qr_code_b64"] = encoded_image

  new_user = models.User(**updated_payload)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  reciepients = [user_email]
  subject = f"Attendance QR Code"
  message = f"""
  <p>Hello {new_user.first_name},</p>
  <br>
  <p>Kindly find your attendance QR Code attached.</p>
  """
  image_path = user_qr_code
  image_name = "QR Code"
  utils.send_email(reciepients, subject, message, image_path)

  return {"status": "success", "data": new_user, "b64_qr_code": encoded_image}


# [...] create admin user
@router.post('/admin', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse, summary="Create Admin User")
# @router.post('/admin', status_code=status.HTTP_201_CREATED)
def create_admin_user(
  first_name: str = Form(...), 
  last_name: str = Form(...),
  email: str = Form(...),
  password: str = Form(...),
  location_id: str | None = Form(None),
  # is_admin: bool | None = Form(None),
  file: UploadFile | None = File(None), 
  current_user: models.User = Depends(utils.get_current_active_user),
  db: Session = Depends(get_db),
):
# def create_user(payload: schemas.CreateUser = Depends(), file: UploadFile | None = None, db: Session = Depends(get_db)):
# def create_user(payload: schemas.CreateUser, file: UploadFile | None = File(...), db: Session = Depends(get_db)):
  payload_dict = {
    "first_name": first_name,
    "last_name": last_name,
    "email": email,
    "location_id": location_id,
    "password": password,
    "is_admin": True,
    # "is_admin": is_admin,
  } # convert payload to dictionary
  print({"payload.dict": payload_dict})
  # payload_dict = payload.dict() # convert payload to dictionary
  # print({"payload": payload, "payload.dict": payload_dict})
  updated_payload = payload_dict

  if not utils.validate_email(email):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email Provided")

  db_user = utils.get_user_by_email(payload_dict["email"], db)
  if db_user:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

  # if payload_dict["password"]:
  # if "password" in payload_dict:
  if password:
    password = payload_dict.pop("password")
    print(payload_dict)
    updated_payload = {**payload_dict, "hashed_password": utils.get_password_hash(password)}
  else: payload_dict.pop("password")

  random_chars = utils.random_string(5) # for generating random strings for image and qr code
  relative_image_path = None
  if file:
    # generate unique name for image
    file_extension = utils.get_file_extension(file.filename)
    relative_image_path = f"./training_images/{first_name}-{email}-{random_chars}{file_extension}"

    # save file to training images folder
    with open(relative_image_path, "wb") as buffer:
      # print(buffer)
      copyfileobj(file.file, buffer)

    # get image and face encodings from uploaded file
    image_encoding, face_encoding = utils.check_face_in_picture(file.file)
    # image_encoding_str = json.dumps(image_encoding.tolist())
    image_encoding_str = json.dumps([]) # Image encoding is not needed
    face_encoding_str = json.dumps(face_encoding.tolist())

    print(relative_image_path)
    # print(relative_image_path, image_encoding, face_encoding)

    # update user instance with image and encodings
    updated_payload = {**updated_payload, "image": relative_image_path, "image_encoding": image_encoding_str, "face_encoding": face_encoding_str}  

  # generate a qr code
  user_email = updated_payload["email"]
  user_qr_code = utils.generate_qr_code(user_email, f"./qr_codes/{user_email}-{random_chars}")

  # generate b64 image of the qr code for display
  encoded_image = None
  if user_qr_code:
    import base64
    # Convert the image to base64 format
    with open(user_qr_code, "rb") as f:
      encoded_image = base64.b64encode(f.read())

  updated_payload["qr_code"] = user_qr_code
  updated_payload["qr_code_content"] = user_email
  updated_payload["qr_code_b64"] = encoded_image

  new_user = models.User(**updated_payload)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  reciepients = [user_email]
  subject = f"Attendance QR Code"
  message = f"""
  <p>Hello {new_user.first_name},</p>
  <br>
  <p>Kindly find your attendance QR Code attached.</p>
  """
  image_path = user_qr_code
  image_name = "QR Code"
  utils.send_email(reciepients, subject, message, image_path)

  return {"status": "success", "data": new_user, "b64_qr_code": encoded_image}


# [...] get user by id
@router.get('/{user_id}', response_model=schemas.UserResponse)
# @router.get('/{user_id}')
def get_user(user_id: str):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  return {"status": "success", "data": user}



# [...] edit user by id
@router.patch('/{user_id}', response_model=schemas.UserResponse)
# @router.patch('/{user_id}')
def update_user(user_id: str, payload: schemas.UpdateUser, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  # update_data = payload.dict(exclude_unset=True)
  # if update_data["password"]: update_data["hashed_password"] = utils.get_password_hash(update_data["password"])

  # if password:
  if "password" in update_data:
    password = update_data.pop("password")
    print(update_data)
    updated_payload = {**update_data, "hashed_password": utils.get_password_hash(password)}

  get_user.filter(models.User.id == user_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)
  return {"status": "success", "data": user}


# [...] upload user photo user by id
@router.patch('/{user_id}/image', response_model=schemas.UserResponse)
# @router.patch('/{user_id}/image')
def update_user(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  # generate unique name for image
  random_chars = utils.random_string(5)
  file_extension = utils.get_file_extension(file.filename)
  relative_image_path = f"./training_images/{user.first_name}-{user.email}-{random_chars}{file_extension}"

  # save file to training images folder
  with open(relative_image_path, "wb") as buffer:
    print(buffer)
    copyfileobj(file.file, buffer)

  # get image and face encodings from uploaded file
  image_encoding, face_encoding = utils.check_face_in_picture(file.file)
  # image_encoding_str = json.dumps(image_encoding.tolist())
  image_encoding_str = json.dumps([]) # Image encoding is not needed
  face_encoding_str = json.dumps(face_encoding.tolist())

  print(relative_image_path, image_encoding, face_encoding)

  # update user instance with image and encodings
  update_data = {"image": relative_image_path, "image_encoding": image_encoding_str, "face_encoding": face_encoding_str}  
  get_user.filter(models.User.id == user_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)

  return {"status": "success", "data": user}



# [...] delete user by id
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')
  get_user.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
