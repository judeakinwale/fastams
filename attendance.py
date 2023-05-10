from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
from datetime import date, timedelta
import numpy as np
import models
import schemas
import utils
import json

router = APIRouter()


# [...] attendance sign in
@router.post('/sign-in', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponse, summary="Attendance Sign In")
# @router.post('/sign-in', status_code=status.HTTP_201_CREATED)
# def create_attendance_history(payload: schemas.AttendanceHistory, file: UploadFile = File(...), db: Session = Depends(get_db)):
def create_attendance_history(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
  # payload_email = payload.dict()["email"]
  payload_email = email
  user = db.query(models.User).filter(models.User.email == payload_email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  if not user.image:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No profile image found. Contact the admin to add an image to your profile.')

  if not user.face_encoding:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No face found in profile image. Contact the admin to update your profile image.')

  location = None
  # # if location is required
  # location = db.query(models.Location).filter(models.Location.id == user.location_id).first()
  # if not location:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location for user with this email: {email} found')

  # check user has recently (today) signed in and not signed out yet
  today = f"{date.today()}"
  tomorrow = f"{date.today() + timedelta(1)}"
  get_attendance_history = db.query(models.AttendanceHistory).filter(
    models.AttendanceHistory.email == email, 
    models.AttendanceHistory.created_at > today, 
    models.AttendanceHistory.created_at < tomorrow,
    models.AttendanceHistory.is_signed_in == True,
    models.AttendanceHistory.is_signed_out == False,
  )
  attendance_history = get_attendance_history.first()

  if attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'You have signed in with this email: {email}. Sign out instead')

  user_face_encoding = np.array(json.loads(user.face_encoding))

  # get image and face encodings from uploaded file
  image_encoding, face_encoding = utils.check_face_in_picture(file.file)
  # image_encoding_str = json.dumps(image_encoding.tolist())
  image_encoding_str = json.dumps([]) # Image encoding is not needed
  face_encoding_str = json.dumps(face_encoding.tolist())

  # check if image matches
  image_matches = utils.check_face_match(user_face_encoding, face_encoding)
  print(image_matches)
  if not image_matches:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Matching face not found. Try Again.')

  # generate unique name for image
  random_chars = utils.random_string(2)
  file_extension = utils.get_file_extension(file.filename)
  relative_image_path = f"./attendance_images/{user.first_name}-{user.email}-{today}-{random_chars}{file_extension}"

  # save file to attendance images folder
  with open(relative_image_path, "wb") as buffer:
    # print(buffer)
    copyfileobj(file.file, buffer)

  # update user instance with image and encodings
  updated_payload = {
    # **payload.dict(),
    "email": email,
    "user_id": user.id,
    "location_id": location.id if location else None,
    "image": relative_image_path, 
    "image_encoding": image_encoding_str, 
    "face_encoding": face_encoding_str, 
    "is_signed_in": True,
  }  

  # new_attendance_history = models.AttendanceHistory(**payload.dict())
  new_attendance_history = models.AttendanceHistory(**updated_payload)
  db.add(new_attendance_history)
  db.commit()
  db.refresh(new_attendance_history)
  return {"status": "success", "data": new_attendance_history}


# [...] attendance sign out
@router.patch('/sign-out', response_model=schemas.AttendanceHistoryResponse, summary="Attendance Sign Out")
# @router.post('/sign-out')
def update_attendance_history(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
  payload_email = email
  user = db.query(models.User).filter(models.User.email == payload_email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  if not user.image:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No profile image found. Contact the admin to add an image to your profile.')

  if not user.face_encoding:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No face found in profile image. Contact the admin to update your profile image.')
  
  today = f"{date.today()}"
  tomorrow = f"{date.today() + timedelta(1)}"
  get_attendance_history = db.query(models.AttendanceHistory).filter(
    models.AttendanceHistory.email == email, 
    models.AttendanceHistory.created_at > today, 
    models.AttendanceHistory.created_at < tomorrow, 
    models.AttendanceHistory.is_signed_out == False,
  )
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this email: {email} found')

  user_face_encoding = np.array(json.loads(user.face_encoding))

  # get image and face encodings from uploaded file
  image_encoding, face_encoding = utils.check_face_in_picture(file.file)
  # image_encoding_str = json.dumps(image_encoding.tolist())
  image_encoding_str = json.dumps([]) # Image encoding is not needed
  face_encoding_str = json.dumps(face_encoding.tolist())

  # check if image matches
  image_matches = utils.check_face_match(user_face_encoding, face_encoding)
  print(image_matches)
  if not image_matches:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Matching face not found. Try Again.')

  update_data = {"is_signed_out": True}
  get_attendance_history.filter(models.AttendanceHistory.id == attendance_history.id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(attendance_history)
  return {"status": "success", "data": attendance_history}



# [...] attendance sign in with qr code
@router.post('/sign-in-qr', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponse, summary="Attendance Sign In with QR")
# @router.post('/sign-in-qr', status_code=status.HTTP_201_CREATED)
# def create_attendance_history(payload: schemas.AttendanceHistory, file: UploadFile = File(...), db: Session = Depends(get_db)):
def create_attendance_history(content: str | None = None, file: UploadFile = File(None), db: Session = Depends(get_db)):
  if not (content or file): 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No QR Code provided. Try again.')
  
  qr_code_content = content # default

  if not content:
    # get qr code and validate content
    cv_file = utils.get_opencv_img_from_buffer(file.file)
    qr_code_content = utils.read_qr_code(cv_file, True)

    # qr_code_content = utils.read_qr_code(file.file)
    print({"qr_code_content": qr_code_content})
    if not utils.validate_email(qr_code_content):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid QR Code. Try again.')

  # payload_email = payload.dict()["email"]
  email = qr_code_content
  user = db.query(models.User).filter(models.User.email == email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  location = None
  # # if location is required
  # location = db.query(models.Location).filter(models.Location.id == user.location_id).first()
  # if not location:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location for user with this email: {email} found')

  # check user has recently (today) signed in and not signed out yet
  today = f"{date.today()}"
  tomorrow = f"{date.today() + timedelta(1)}"
  get_attendance_history = db.query(models.AttendanceHistory).filter(
    models.AttendanceHistory.email == email, 
    models.AttendanceHistory.created_at > today, 
    models.AttendanceHistory.created_at < tomorrow,
    models.AttendanceHistory.is_signed_in == True,
    models.AttendanceHistory.is_signed_out == False,
  )
  attendance_history = get_attendance_history.first()

  if attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'You have signed in with this email: {email}. Sign out instead')

  if not content:
    # generate unique name for qr code image
    random_chars = utils.random_string(2)
    file_extension = utils.get_file_extension(file.filename)
    relative_image_path = f"./attendance_qr_codes/{user.first_name}-{user.email}-{today}-{random_chars}{file_extension}"

    # save file to attendance images folder
    with open(relative_image_path, "wb") as buffer:
      # print(buffer)
      copyfileobj(file.file, buffer)

  # update user instance with image and encodings
  updated_payload = {
    # **payload.dict(),
    "email": email,
    "user_id": user.id,
    "location_id": location.id if location else None,
    "qr_code": relative_image_path if not content else None, 
    "qr_code_content": qr_code_content, 
    "is_signed_in": True,
  }  


  # new_attendance_history = models.AttendanceHistory(**payload.dict())
  new_attendance_history = models.AttendanceHistory(**updated_payload)
  db.add(new_attendance_history)
  db.commit()
  db.refresh(new_attendance_history)
  return {"status": "success", "data": new_attendance_history}


# [...] attendance sign out with qr code
@router.post('/sign-out-qr', response_model=schemas.AttendanceHistoryResponse, summary="Attendance Sign Out with QR")
# @router.post('/sign-out-qr')
def update_attendance_history(content: str | None = None, file: UploadFile = File(None), db: Session = Depends(get_db)):
  if not (content or file): 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No QR Code provided. Try again.')

  qr_code_content = content # default

  if not content:
    # get qr code and validate content
    cv_file = utils.get_opencv_img_from_buffer(file.file)
    qr_code_content = utils.read_qr_code(cv_file, True)

    # qr_code_content = utils.read_qr_code(file)
    print({"qr_code_content": qr_code_content})
    if not utils.validate_email(qr_code_content):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid QR Code. Try again.')

  email = qr_code_content

  # check user has recently (today) signed in and not signed out yet
  today = f"{date.today()}"
  tomorrow = f"{date.today() + timedelta(1)}"
  get_attendance_history = db.query(models.AttendanceHistory).filter(
    models.AttendanceHistory.email == email, 
    models.AttendanceHistory.created_at > today, 
    models.AttendanceHistory.created_at < tomorrow, 
    models.AttendanceHistory.is_signed_out == False,
  )
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this email: {email} found')

  update_data = {"is_signed_out": True}
  get_attendance_history.filter(models.AttendanceHistory.id == attendance_history.id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(attendance_history)
  return {"status": "success", "data": attendance_history}



# [...] get all attendance_history
@router.get('/', response_model=schemas.ListAttendanceHistoryResponse)
# @router.get('/')
def get_attendance_history(db: Session = Depends(get_db), limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.email.contains(search)).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(attendance_history), 'data': attendance_history}


# [...] create attendance_history
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_attendance_history(payload: schemas.BaseAttendanceHistory, db: Session = Depends(get_db)):
    new_attendance_history = models.AttendanceHistory(**payload.dict())
    db.add(new_attendance_history)
    db.commit()
    db.refresh(new_attendance_history)
    return {"status": "success", "data": new_attendance_history}


# [...] get attendance_history by id
@router.get('/{attendance_history_id}', response_model=schemas.AttendanceHistoryResponse)
# @router.get('/{attendance_history_id}')
def get_attendance_history(attendance_history_id: str):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_history_id)
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_history_id} found')

  return {"status": "success", "data": attendance_history}



# [...] edit attendance_history by id
@router.patch('/{attendance_history_id}', response_model=schemas.AttendanceHistoryResponse)
# @router.patch('/{attendance_history_id}')
def update_attendance_history(attendance_history_id: str, payload: schemas.AttendanceHistory, db: Session = Depends(get_db)):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_history_id)
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_history_id} found')

  update_data = payload.dict(exclude_unset=True)
  get_attendance_history.filter(models.AttendanceHistory.id == attendance_history_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(attendance_history)
  return {"status": "success", "data": attendance_history}


# [...] delete attendance_history by id
@router.delete('/{attendance_history_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_history(attendance_history_id: str, db: Session = Depends(get_db)):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_history_id)
  attendance_history = get_attendance_history.first()
  if not attendance_history:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {id} found')
  get_attendance_history.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
