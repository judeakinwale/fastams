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

router = APIRouter()


# [...] get all settings
@router.get('/', response_model=schemas.ListSettingsResponse)
# @router.get('/')
def get_settings(limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  settings = [utils.mongo_res(setting) for setting in models.Settings.find()]
  return {'status': 'success', 'count': len(settings), 'data': settings}


# [...] create settings
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SettingsResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_settings(payload: schemas.Settings):
  payload = payload.dict(exclude_unset=True)
  payload.update({'created_at': datetime.now(), 'updated_at': datetime.now()})
  print({"payload": payload})

  userPayload = {
    'first_name': 'admin',
    'last_name': 'admin',
    'email': 'admin@admin.com',
    'hashed_password': utils.get_password_hash('admin'),
    'is_admin': True,
    'is_active': True,
    'created_at': datetime.now(), 
    'updated_at': datetime.now(),
  }

  # ensure only one setting is created
  settings = utils.mongo_res(models.Settings.find_one_and_update({}, {"$set": payload}, return_document=ReturnDocument.AFTER, upsert=True))
  user = utils.mongo_res(models.User.find_one_and_update({"email": "admin@admin.com"}, {"$set": userPayload}, return_document=ReturnDocument.AFTER, upsert=True))
  
  return {"status": "success", "data": settings, "message": "Settings Created"}


# [...] get settings by id
@router.get('/{settings_id}', response_model=schemas.SettingsResponse)
# @router.get('/{settings_id}')
def get_settings(settings_id: str):
  settings = utils.mongo_res(models.Settings.find_one({"_id": ObjectId(settings_id)}))
  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {settings_id} found')

  return {"status": "success", "data": settings}



# [...] edit settings by id
@router.patch('/{settings_id}', response_model=schemas.SettingsResponse)
# @router.patch('/{settings_id}')
def update_settings(settings_id: str, payload: schemas.Settings):
  payload = payload.dict(exclude_unset=True)
  payload.update({'updated_at': datetime.now()})
  print({"payload": payload})

  filter = {"_id": ObjectId(settings_id)}
  
  settings = utils.mongo_res(models.Settings.find_one_and_update(filter, {"$set": payload}, return_document=ReturnDocument.AFTER))
  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {settings_id} found')

  return {"status": "success", "data": settings}


# [...] delete settings by id
@router.delete('/{settings_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_settings(settings_id: str):
  settings = utils.mongo_res(models.Settings.find_one_and_delete({"_id": ObjectId(settings_id)}))
  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {settings_id} found')
    
  return Response(status_code=status.HTTP_204_NO_CONTENT)
