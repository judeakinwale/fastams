from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from datetime import date, timedelta
import models
import schemas
import utils

router = APIRouter()


# [...] attendance sign in
# @router.post('/sign-in', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistory)
@router.post('/sign-in', status_code=status.HTTP_201_CREATED)
# def create_attendance_history(payload: schemas.AttendanceHistory, file: UploadFile = File(...), db: Session = Depends(get_db)):
def create_attendance_history(email: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
  # payload_email = payload.dict()["email"]
  payload_email = email
  user = db.query(models.User).filter(models.User.email == payload_email).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  location = db.query(models.Location).filter(models.Location.id == user.location_id).first()
  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location for user with this email: {email} found')

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
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'You have signed in with this email: {email} found. Sign out instead')

  
  # # generate unique name for image
  # random_chars = utils.random_string(5)
  # file_extension = utils.get_file_extension(file.filename)
  # relative_image_path = f"./training_images/{user.first_name}-{user.email}-{random_chars}.{file_extension}"

  # # save file to training images folder
  # with open(relative_image_path, "w") as buffer:
  #   print(buffer)
  #   copyfileobj(file.file, buffer)

  # get image and face encodings from uploaded file
  image_encoding, face_encoding = utils.check_face_in_picture(file.file)

  # check if image matches
  image_matches = utils.check_face_match(user.face_encoding, face_encoding)
  if not image_matches:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Matching face not found. Try Again.')

  # update user instance with image and encodings
  updated_payload = {
    # **payload.dict(),
    "email": email,
    "user_id": user.id,
    "location_id": location.id,
    "image": relative_image_path, 
    "image_encoding": image_encoding, 
    "face_encoding": face_encoding, 
    "is_signed_in": True,
  }  

  # new_attendance_history = models.AttendanceHistory(**payload.dict())
  new_attendance_history = models.AttendanceHistory(**updated_payload)
  db.add(new_attendance_history)
  db.commit()
  db.refresh(new_attendance_history)
  return {"status": "success", "data": new_attendance_history}


# [...] attendance sign out
# @router.patch('/sign-out', response_model=schemas.AttendanceHistory)
@router.post('/sign-out')
def update_attendance_history(email: str, db: Session = Depends(get_db)):
  today = f"{date.today()}"
  tomorrow = f"{date.today() + timedelta(1)}"
  get_attendance_history = db.query(models.AttendanceHistory).filter(
    models.AttendanceHistory.email == email, 
    models.AttendanceHistory.created_at > today, 
    models.AttendanceHistory.created_at < tomorrow, 
  )
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this email: {email} found')

  update_data = {"is_signed_out": True}
  get_attendance_history.filter(models.AttendanceHistory.id == attendance_history_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(attendance_history)
  return {"status": "success", "data": attendance_history}


# [...] get all attendance_history
# @router.get('/', response_model=list[schemas.AttendanceHistory])
@router.get('/')
def get_attendance_history(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.email.contains(search)).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(attendance_history), 'data': attendance_history}


# [...] create attendance_history
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistory)
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_attendance_history(payload: schemas.AttendanceHistory, db: Session = Depends(get_db)):
    new_attendance_history = models.AttendanceHistory(**payload.dict())
    db.add(new_attendance_history)
    db.commit()
    db.refresh(new_attendance_history)
    return {"status": "success", "data": new_attendance_history}


# [...] get attendance_history by id
# @router.get('/{attendance_history_id}', response_model=schemas.AttendanceHistory)
@router.get('/{attendance_history_id}')
def get_attendance_history(attendance_history_id: str):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_history_id)
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_history_id} found')

  return {"status": "success", "data": attendance_history}



# [...] edit attendance_history by id
# @router.patch('/{attendance_history_id}', response_model=schemas.AttendanceHistory)
@router.patch('/{attendance_history_id}')
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
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_history_id).first()
  attendance_history = get_attendance_history
  if not attendance_history:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {id} found')
  get_attendance_history.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
