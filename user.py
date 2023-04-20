from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
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
# @router.get('/', response_model=list[schemas.User])
@router.get('/')
def get_users(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  users = db.query(models.User).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(users), 'data': users}


# [...] create user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.CreateUser, db: Session = Depends(get_db)):
    payload_dict = payload.dict() # convert payload to dictionary
    print({"payload": payload, "payload.dict": payload_dict})

    db_user = utils.get_user_by_email(payload_dict["email"], db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password = payload_dict.pop("password")
    print(payload_dict)
    updated_payload = {**payload_dict, "hashed_password": utils.get_password_hash(password)}

    new_user = models.User(**updated_payload)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "data": new_user}


# [...] get user by id
# @router.get('/{user_id}', response_model=schemas.User)
@router.get('/{user_id}')
def get_user(user_id: str):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  return {"status": "success", "data": user}



# [...] edit user by id
# @router.patch('/{user_id}', response_model=schemas.User)
@router.patch('/{user_id}')
def update_user(user_id: str, payload: schemas.User, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == user_id)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {user_id} found')

  update_data = payload.dict(exclude_unset=True)
  if update_data["password"]: update_data["hashed_password"] = utils.get_password_hash(update_data["password"])

  get_user.filter(models.User.id == user_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)
  return {"status": "success", "data": user}


# [...] upload user photo user by id
# @router.patch('/{user_id}/image', response_model=schemas.User)
@router.patch('/{user_id}/image')
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
  get_user = db.query(models.User).filter(models.User.id == user_id).first()
  user = get_user
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {id} found')
  get_user.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
