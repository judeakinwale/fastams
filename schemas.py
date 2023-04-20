from datetime import datetime
from typing import List
from pydantic import BaseModel


class AttendanceHistory(BaseModel):
  id: int | None = None
  # id: str | None = None
  email: str
  user_id: int
  location_id: int
  phone: str | None = None
  image: str | None = None
  image_encoding: str | None = None
  face_encoding: str | None = None
  is_signed_in: bool = False
  is_signed_out: bool = False
  is_active: bool = True
  created_at: datetime | None = None
  updated_at: datetime | None = None

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True

class ListAttendanceHistoryResponse(BaseModel):
  status: str
  count: int
  data: List[AttendanceHistory]


class AttendanceHistoryResponse(BaseModel):
  status: str
  data: AttendanceHistory



class User(BaseModel):
  id: int | None = None
  # id: str | None = None
  first_name: str
  last_name: str
  email: str
  hashed_password: str | None = None
  phone: str | None = None
  image: str | None = None
  image_encoding: str | None = None
  face_encoding: str | None = None
  location_id: int
  is_active: bool = True
  created_at: datetime | None = None
  updated_at: datetime | None = None
  attendance_history: List[AttendanceHistory] | None = []

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class CreateUser(User):
  password: str


class ListUserResponse(BaseModel):
  status: str
  count: int
  data: List[User]


class UserResponse(BaseModel):
  status: str
  data: User



class Location(BaseModel):
  id: int | None = None
  # id: str | None = None
  name: str
  address: str
  description: str | None = None
  phone: str | None = None
  is_active: bool = True
  created_at: datetime | None = None
  updated_at: datetime | None = None
  attendance_history: List[AttendanceHistory] | None = []
  # users: User | None = None
  users: List[User] | None = []

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True

class ListLocationResponse(BaseModel):
  status: str
  count: int
  data: List[Location]


class LocationResponse(BaseModel):
  status: str
  data: Location
