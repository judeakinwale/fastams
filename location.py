from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
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

router = APIRouter()


def get_detailed_location(location):
  location = utils.mongo_res(location)

  attendance_history = [utils.mongo_res(attendance) for attendance in models.AttendanceHistory.find({'location_id': location['id']})]
  location['attendance_history'] = attendance_history

  users = [utils.mongo_res(user) for user in models.User.find({'location_id': location['id']})]
  location['users'] = users

  return location


# [...] get all locations
@router.get('/', response_model=schemas.ListLocationResponse)
def get_locations(limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit
  filter = {"$text": {"$search": search}} if search else {}

  locations = [get_detailed_location(location) for location in models.Location.find(filter).limit(limit).skip(skip)]
  # print(locations)
  
  return {'status': 'success', 'count': len(locations), 'data': locations}


# [...] create location
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
def create_location(payload: schemas.BaseLocation):
  payload = payload.dict(exclude_unset=True)
  payload.update({'createdAt': datetime.now(), "updated_at": datetime.now(),})
  print({"payload": payload})

  created_id = models.Location.insert_one(payload).inserted_id
  location = get_detailed_location(models.Location.find_one({'_id': created_id}))

  return {"status": "success", "data": location}


# [...] get location by id
@router.get('/{location_id}', response_model=schemas.LocationResponse)
def get_location(location_id: str):
  location = get_detailed_location(models.Location.find_one({'_id': ObjectId(location_id)}))
  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {location_id} found')

  return {"status": "success", "data": location}


# [...] edit location by id
@router.patch('/{location_id}', response_model=schemas.LocationResponse)
def update_location(location_id: str, payload: schemas.UpdateLocation):
  payload = payload.dict(exclude_unset=True)
  payload.update({'updated_at': datetime.now()})
  print({"payload": payload})

  location = get_detailed_location(models.Location.find_one_and_update({'_id': ObjectId(location_id)}, {'$set': payload}, return_document=ReturnDocument.AFTER))
  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {location_id} found')

  return {"status": "success", "data": location}


# [...] delete location by id
@router.delete('/{location_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: str):
  location = utils.mongo_res(models.Location.find_one_and_delete({'_id': ObjectId(location_id)}))
  if not location:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {location_id} found')

  return Response(status_code=status.HTTP_204_NO_CONTENT)
