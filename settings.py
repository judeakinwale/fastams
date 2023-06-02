from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
import models
import schemas
import utils

router = APIRouter()


# [...] get all settings
@router.get('/', response_model=schemas.SettingsResponse)
# @router.get('/')
def get_settings(db: Session = Depends(get_db), limit: int = 1000000000000, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  # settings = db.query(models.Settings).filter(models.Settings.name.contains(search)).limit(limit).offset(skip).all()
  settings = db.query(models.Settings).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(settings), 'data': settings}


# [...] create settings
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.SettingsResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_settings(payload: schemas.Settings, db: Session = Depends(get_db)):
  get_settings = db.query(models.Settings)
  settings = get_settings.first()

  # ensure only one setting is created
  if settings:
    update_data = payload.dict(exclude_unset=True)
    get_settings.filter(models.Settings.id == settings.id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(settings)
    return {"status": "success", "data": settings, "message": "Settings Updated"}

  new_settings = models.Settings(**payload.dict())
  db.add(new_settings)
  db.commit()
  db.refresh(new_settings)
  return {"status": "success", "data": new_settings, "message": "Settings Created"}


# [...] get settings by id
@router.get('/{settings_id}', response_model=schemas.SettingsResponse)
# @router.get('/{settings_id}')
def get_settings(settings_id: str, db: Session = Depends(get_db)):
  get_settings = db.query(models.Settings).filter(models.Settings.id == settings_id)
  settings = get_settings.first()

  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {settings_id} found')

  return {"status": "success", "data": settings}



# [...] edit settings by id
@router.patch('/{settings_id}', response_model=schemas.SettingsResponse)
# @router.patch('/{settings_id}')
def update_settings(settings_id: str, payload: schemas.Settings, db: Session = Depends(get_db)):
  get_settings = db.query(models.Settings).filter(models.Settings.id == settings_id)
  settings = get_settings.first()

  if not settings:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {settings_id} found')

  update_data = payload.dict(exclude_unset=True)
  get_settings.filter(models.Settings.id == settings_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(settings)
  return {"status": "success", "data": settings}


# [...] delete settings by id
@router.delete('/{settings_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_settings(settings_id: str, db: Session = Depends(get_db)):
  get_settings = db.query(models.Settings).filter(models.Settings.id == settings_id).first()
  settings = get_settings.first()
  if not settings:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No settings with this id: {id} found')
  get_settings.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
