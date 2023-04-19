from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from sqlite_database import get_db, Base # for sqlite db
# from database import get_db, Base # for postgres db
import models
import schemas

router = APIRouter()


# [...] get all users
# @router.get('/', response_model=list[schemas.User])
@router.get('/')
def get_users(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
  skip = (page - 1) * limit

  users = db.query(models.User).filter(models.User.email.contains(search)).limit(limit).offset(skip).all()
  # users = db.query(models.User).all()
  print(len(users))
  return {'status': 'success', 'count': len(users), 'data': users}


# [...] create user
# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**payload.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "data": new_user}


# [...] get user by id
# @router.get('/{userId}', response_model=schemas.User)
@router.get('/{userId}')
def get_user(userId: str):
  get_user = db.query(models.User).filter(models.User.id == userId)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {userId} found')

  return {"status": "success", "data": user}



# [...] edit user by id
# @router.patch('/{userId}', response_model=schemas.User)
@router.patch('/{userId}')
def update_user(userId: str, payload: schemas.User, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == userId)
  user = get_user.first()

  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {userId} found')

  update_data = payload.dict(exclude_unset=True)
  get_user.filter(models.User.id == userId).update(update_data, synchronize_session=False)
  db.commit()
  db.refresh(user)
  return {"status": "success", "data": user}


# [...] delete user by id
@router.delete('/{userId}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(userId: str, db: Session = Depends(get_db)):
  get_user = db.query(models.User).filter(models.User.id == userId).first()
  user = get_user
  if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user with this id: {id} found')
  get_user.delete(synchronize_session=False)
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)
