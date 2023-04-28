from fastapi import Depends, HTTPException, status, APIRouter, Response, UploadFile, File
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
from shutil import copyfileobj
import models
import schemas
import utils

router = APIRouter()


# [...] get all locations
@router.get('/', response_model=schemas.ListLocationResponse)
# @router.get('/')
def get_locations(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  locations = db.query(models.Location).filter(models.Location.name.contains(search)).limit(limit).offset(skip).all()
  return {'status': 'success', 'count': len(locations), 'data': locations}


# [...] create location
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.LocationResponse)
# @router.post('/', status_code=status.HTTP_201_CREATED)
def create_location(payload: schemas.BaseLocation, db: Session = Depends(get_db)):
    print(payload)
    new_location = models.Location(**payload.dict())
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return {"status": "success", "data": new_location}


# [...] get location by id
@router.get('/{location_id}', response_model=schemas.LocationResponse)
# @router.get('/{location_id}')
def get_location(location_id: str):
  get_location = db.query(models.Location).filter(models.Location.id == location_id)
  location = get_location.first()

  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {location_id} found')

  return {"status": "success", "data": location}



# [...] edit location by id
@router.patch('/{location_id}', response_model=schemas.LocationResponse)
# @router.patch('/{location_id}')
def update_location(location_id: str, payload: schemas.Location, db: Session = Depends(get_db)):
  get_location = db.query(models.Location).filter(models.Location.id == location_id)
  location = get_location.first()

  if not location:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {location_id} found')

  update_data = payload.dict(exclude_unset=True)
  get_location.filter(models.Location.id == location_id).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(location)
  return {"status": "success", "data": location}


# [...] delete location by id
@router.delete('/{location_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id: str, db: Session = Depends(get_db)):
  get_location = db.query(models.Location).filter(models.Location.id == location_id).first()
  location = get_location.first()
  if not location:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No location with this id: {id} found')
  get_location.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
