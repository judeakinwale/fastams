from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
from datetime import date, timedelta
from bson.objectid import ObjectId
from datetime import datetime
from pymongo import ReturnDocument
import numpy as np
import models
import schemas
import utils
import json

router = APIRouter()



def get_detailed_attendance_history(attendance_history):
  attendance_history = utils.mongo_res(attendance_history)

  user = utils.mongo_res(models.User.find_one({'_id': ObjectId(attendance_history['user_id'])}))
  attendance_history['user'] = user

  location = utils.mongo_res(models.Location.find_one({'_id': ObjectId(attendance_history['location_id'])}))
  attendance_history['location'] = location

  print("user_id", attendance_history['user_id'], user)
  print("location_id", attendance_history['location_id'], location)

  return attendance_history


def check_valid_user_for_facial_recognition(email: str):
  user = utils.mongo_res(models.User.find_one({"email": email}))
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  if not user['image']:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No profile image found. Contact the admin to add an image to your profile.')

  if not user['face_encoding']:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No face found in profile image. Contact the admin to update your profile image.')

  return user


def check_face_using_facial_recognition(user: schemas.User, file: UploadFile = File(...)):
  # get saved face encoding
  user_face_encoding = np.array(json.loads(user['face_encoding']))

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

  return {
    "image_encoding": image_encoding,
    "face_encoding": face_encoding,
    "image_encoding_str": image_encoding_str,
    "face_encoding_str": face_encoding_str,
  }


def save_attendance_image_file(first_name: str = "anon", email: str = "anon@test.com", file: UploadFile = File(None), is_qr_code: bool = True, folder_name: str = "attendance_images"):
  # save qr code to storage
  if file:
    # generate unique name for qr code image
    today = f"{date.today()}"
    random_chars = utils.random_string(2)
    file_extension = utils.get_file_extension(file.filename)
    folder_name = "attendance_qr_codes" if is_qr_code else folder_name
    relative_image_path = f"./{folder_name}/{first_name}-{email}-{today}-{random_chars}{file_extension}"

    # save file to appriopriate folder {folder_name}
    with open(relative_image_path, "wb") as buffer:
      # print(buffer)
      copyfileobj(file.file, buffer)

    return relative_image_path



def get_user_and_email_from_qr_code(content: str | None = None, file: UploadFile = File(None)):
  # use_qr_code = utils.is_qr_code_used()
  # if not use_qr_code:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location found for your account. Kindly contact the admin.')

  if not (content or file): 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No QR Code provided. Try again.')
  
  qr_code_content = content # default

  if not content:
    # get qr code and validate  content
    cv_file = utils.get_opencv_img_from_buffer(file.file)
    qr_code_content = utils.read_qr_code(cv_file, True)

    print({"qr_code_content": qr_code_content})
    if not utils.validate_email(qr_code_content):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid QR Code. Try again.')

  email = qr_code_content
  user = utils.mongo_res(models.User.find_one({'email': email}))
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this email: {email} found')

  if file: 
    save_attendance_image_file(user['first_name'], user['email'], file)

  return user, email


def check_recent_attendance_history(email: str, is_sign_out: bool = False):
  # check user has recently (today) signed in and not signed out yet
  # convert date to datetime for pymongo
  today = datetime.combine(date.today(), datetime.min.time())
  tomorrow = datetime.combine((date.today() + timedelta(1)), datetime.min.time())
  attendance_history = utils.mongo_res(models.AttendanceHistory.find_one({
    'email': email,
    'created_at': {'$gte': today, '$lte': tomorrow},
    'is_signed_in': True,
    'is_signed_out': False,

  }))

  if is_sign_out:
    # throw error if signing out and no attendance history found
    if not attendance_history:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this email: {email} found')
    return attendance_history

  if attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'You have signed in with this email: {email}. Sign out instead')


def check_location(location_id: str, email: str, long: str | None = None, lat: str | None = None, is_sign_out: bool = False):  
  location = None
  use_location = utils.is_location_used()
  attendance_type = "Signout" if is_sign_out else "Signin"
  if use_location:
    if not location_id:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location found for your account. Kindly contact the admin.')

    location = utils.mongo_res(models.Location.find_one({'_id': ObjectId(location_id)}))
    if not location:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location for user with this email: {email} found. Kindly contact the admin.')

    if not (long or lat):
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{attendance_type} location not provided!')
    
    is_location_match = utils.check_matching_location(location, float(long), float(lat))
    if not is_location_match:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'You are not allowed to {attendance_type} from this location')



# [...] attendance sign in
@router.post('/sign-in', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponseWithUser, summary="Attendance Sign In")
# @router.post('/sign-in', status_code=status.HTTP_201_CREATED)
# def create_attendance_history(payload: schemas.AttendanceHistory, file: UploadFile = File(...)):
def create_attendance_history(email: str, file: UploadFile = File(...), long: str | None = None, lat: str | None = None):
  use_facial_recognition = utils.is_facial_recognition_used()
  if not use_facial_recognition:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Facial Recognition Clockin and Clockout is disabled. Kindly contact the admin.')

  user = check_valid_user_for_facial_recognition(email)

  attendance_history = check_recent_attendance_history(email)

  location = check_location(user['location_id'], email, long, lat)

  face_check_result = check_face_using_facial_recognition(user, file)

  relative_image_path = save_attendance_image_file(user["first_name"], email, file, False)

  # update user instance with image and encodings
  payload = {
    "email": email,
    "user_id": user["id"],
    "location_id": location["id"] if location else None,
    "image": relative_image_path, 
    "image_encoding": face_check_result["image_encoding_str"], 
    "face_encoding": face_check_result["face_encoding_str"], 
    "is_signed_in": True,
    "is_signed_out": False,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
  }  

  created_id = models.AttendanceHistory.insert_one(payload).inserted_id
  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one({'_id': ObjectId(created_id)}))
  print({"attendance_history": attendance_history})

  return {"status": "success", "data": attendance_history}



# [...] attendance sign out
@router.patch('/sign-out', response_model=schemas.AttendanceHistoryResponseWithUser, summary="Attendance Sign Out")
# @router.post('/sign-out')
def update_attendance_history(email: str, file: UploadFile = File(...), long: str | None = None, lat: str | None = None):
  use_facial_recognition = utils.is_facial_recognition_used()
  if not use_facial_recognition:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Facial Recognition Clockin and Clockout is disabled. Kindly contact the admin.')

  user = check_valid_user_for_facial_recognition(email)

  attendance_history = check_recent_attendance_history(email, True)

  location = check_location(user['location_id'], email, long, lat, True)

  face_check_result = check_face_using_facial_recognition(user, file)

  payload = {"is_signed_out": True, "updated_at": datetime.now()}

  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one_and_update({'_id': ObjectId(attendance_history["id"])}, {'$set': payload}, return_document=ReturnDocument.AFTER))
  return {"status": "success", "data": attendance_history}




# [...] attendance sign in with qr code
@router.post('/sign-in-qr', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponseWithUser, summary="Attendance Sign In with QR")
def create_attendance_history(content: str | None = None, file: UploadFile = File(None), long: str | None = None, lat: str | None = None):
  use_qr_code = utils.is_qr_code_used()
  if not use_qr_code:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'QR Code Clockin and Clockout is disabled. Kindly contact the admin.')

  user, email = get_user_and_email_from_qr_code(content, file)

  attendance_history = check_recent_attendance_history(email)

  location = check_location(user['location_id'], email, long, lat)

  relative_image_path = save_attendance_image_file(user["first_name"], email, file)

  # update user instance with image and encodings
  payload = {
    "email": email,
    "user_id": user["id"],
    "location_id": location["id"] if location else None,
    "qr_code": relative_image_path if not content else None, 
    "qr_code_content": email, 
    "is_signed_in": True,
    "is_signed_out": False,
    "created_at": datetime.now(),
    "updated_at": datetime.now(),
  }  

  created_id = models.AttendanceHistory.insert_one(payload).inserted_id
  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one({'_id': ObjectId(created_id)}))
  print({"attendance_history": attendance_history})

  return {"status": "success", "data": attendance_history}


# [...] attendance sign out with qr code
@router.post('/sign-out-qr', response_model=schemas.AttendanceHistoryResponseWithUser, summary="Attendance Sign Out with QR")
# @router.post('/sign-out-qr')
def update_attendance_history(content: str | None = None, file: UploadFile = File(None), long: str | None = None, lat: str | None = None):
  use_qr_code = utils.is_qr_code_used()
  if not use_qr_code:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'QR Code Clockin and Clockout is disabled. Kindly contact the admin.')

  user, email = get_user_and_email_from_qr_code(content, file)

  attendance_history = check_recent_attendance_history(email, True)

  location = check_location(user['location_id'], email, long, lat, True)

  payload = {"is_signed_out": True, "updated_at": datetime.now()}

  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one_and_update({'_id': ObjectId(attendance_history["id"])}, {'$set': payload}, return_document=ReturnDocument.AFTER))
  return {"status": "success", "data": attendance_history}



# [...] get all attendance_history
@router.get('/', response_model=schemas.ListAttendanceHistoryResponseWithUser)
# @router.get('/')
def get_attendance_histories(db: Session = Depends(get_db), limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit
  filter = {"$text": {"$search": search}} if search else {}
  
  # attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.email.contains(search)).limit(limit).offset(skip).all()
  attendance_history = [get_detailed_attendance_history(attendance) for attendance in models.AttendanceHistory.find(filter).limit(limit).skip(skip)]
  print(attendance_history)
  return {'status': 'success', 'count': len(attendance_history), 'data': attendance_history}


# [...] create attendance_history
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.AttendanceHistoryResponseWithUser)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_attendance_history(payload: schemas.BaseAttendanceHistory):
  payload = payload.dict(exclude_unset=True)
  payload.update({'created_at': datetime.now(), 'updated_at': datetime.now()})
  print({"payload": payload})

  created_id = models.AttendanceHistory.insert_one(payload).inserted_id
  attendance_history = utils.mongo_res(models.AttendanceHistory.find_one({'_id': ObjectId(created_id)}))
  return {"status": "success", "data": attendance_history}


# [...] get attendance_history by id
@router.get('/{attendance_history_id}', response_model=schemas.AttendanceHistoryResponseWithUser)
# @router.get('/{attendance_history_id}')
def get_attendance_history(attendance_history_id: str):
  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one({'_id': ObjectId(attendance_history_id)}))
  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_history_id} found')

  return {"status": "success", "data": attendance_history}



# [...] edit attendance_history by id
@router.patch('/{attendance_history_id}', response_model=schemas.AttendanceHistoryResponseWithUser)
def update_attendance_history(attendance_history_id: str, payload: schemas.UpdateAttendanceHistory):
  payload = payload.dict(exclude_unset=True)
  payload.update({'updated_at': datetime.now()})
  print({"payload": payload})

  attendance_history = get_detailed_attendance_history(models.AttendanceHistory.find_one_and_update({'_id': ObjectId(attendance_history_id)}, {'$set': payload}, return_document=ReturnDocument.AFTER))
  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_history_id} found')

  return {"status": "success", "data": attendance_history}


# [...] delete attendance_history by id
@router.delete('/{attendance_history_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_history(attendance_history_id: str):
  attendance_history = utils.mongo_res(models.AttendanceHistory.find_one_and_delete({'_id': ObjectId(attendance_history_id)}))
  if not attendance_history:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {id} found')

  return Response(status_code=status.HTTP_204_NO_CONTENT)
