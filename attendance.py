from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
import models
import schemas

router = APIRouter()


# [...] get all attendance_history
# @router.get('/', response_model=list[schemas.AttendanceHistory])
@router.get('/')
def get_attendance_history(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.email.contains(search)).limit(limit).offset(skip).all()
  # attendance_history = db.query(models.AttendanceHistory).all()
  print(len(attendance_history))
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
# @router.get('/{attendance_historyId}', response_model=schemas.AttendanceHistory)
@router.get('/{attendance_historyId}')
def get_attendance_history(attendance_historyId: str):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_historyId)
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_historyId} found')

  return {"status": "success", "data": attendance_history}



# [...] edit attendance_history by id
# @router.patch('/{attendance_historyId}', response_model=schemas.AttendanceHistory)
@router.patch('/{attendance_historyId}')
def update_attendance_history(attendance_historyId: str, payload: schemas.AttendanceHistory, db: Session = Depends(get_db)):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_historyId)
  attendance_history = get_attendance_history.first()

  if not attendance_history:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {attendance_historyId} found')

  update_data = payload.dict(exclude_unset=True)
  get_attendance_history.filter(models.AttendanceHistory.id == attendance_historyId).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(attendance_history)
  return {"status": "success", "data": attendance_history}


# [...] delete attendance_history by id
@router.delete('/{attendance_historyId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_history(attendance_historyId: str, db: Session = Depends(get_db)):
  get_attendance_history = db.query(models.AttendanceHistory).filter(models.AttendanceHistory.id == attendance_historyId).first()
  attendance_history = get_attendance_history
  if not attendance_history:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No attendance_history with this id: {id} found')
  get_attendance_history.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
