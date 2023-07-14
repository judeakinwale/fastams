from datetime import datetime
from typing import List, Any
from pydantic import BaseModel, Field
from json import dumps
# from bson import ObjectId
from datetime import datetime


class GenericResponse(BaseModel):
  status: str
  data: dict | None = None
  message: str | None = None


class BaseAttendanceHistory(BaseModel):
  email: str
  user_id: str
  location_id: str | None = None
  image: str | None = None
  qr_code: str | None = None
  is_active: bool = True
  updated_at: datetime | None = datetime.now()

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class UpdateAttendanceHistory(BaseAttendanceHistory):
  email: str | None = None
  user_id: str | None = None
  updated_at: datetime | None = datetime.now()


class AttendanceHistory(BaseAttendanceHistory):
  _id: str | None = None # mongo id
  id: str | None = None
  phone: str | None = None
  # image: str | None = None
  image_encoding: str | None = None
  face_encoding: str | None = None
  # qr_code: str | None = None
  qr_code_content: str | None = None
  is_signed_in: bool = False
  is_signed_out: bool = False
  is_signed_in_late: bool = False
  is_signed_out_early: bool = False
  is_signed_out_overtime: bool = False
  created_at: datetime | None = None
  updated_at: datetime | None = None


class ListAttendanceHistoryResponse(BaseModel):
  status: str
  count: int
  data: List[AttendanceHistory]


class AttendanceHistoryResponse(BaseModel):
  status: str
  data: AttendanceHistory



class BaseUser(BaseModel):
  first_name: str
  last_name: str
  email: str
  image: str | None = None
  location_id: str | None = None
  is_admin: bool = False
  is_active: bool = True
  is_on_leave: bool = False
  updated_at: datetime | None = datetime.now()

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class CreateUser(BaseUser):
  password: str | None = None
  hashed_password: str | None = None
  created_at: datetime | None = datetime.now()
  # updated_at: datetime = datetime.now()


class UpdateUser(CreateUser):
  first_name: str | None = None
  last_name: str | None = None
  email: str | None = None
  updated_at: datetime = datetime.now()


class ResetPassword(BaseModel):
  password: str


class User(BaseUser):
  _id: str | None = None # mongo id
  id: str | None = None
  hashed_password: str | None = None
  phone: str | None = None
  image_encoding: str | None = None
  face_encoding: str | None = None
  qr_code: str | None = None
  qr_code_content: str | None = None
  qr_code_b64: str | None = None
  created_at: datetime | None = None
  updated_at: datetime | None = None
  reset_password_token: str | None = None
  reset_token_expire: datetime | None = None
  attendance_history: List[AttendanceHistory] | None = []


class ListUserResponse(BaseModel):
  status: str
  count: int
  data: List[User]


class UserResponse(BaseModel):
  status: str
  data: User
  b64_qr_code: str | None = None


class UserLogin(BaseModel):
  email: str
  password: str


class ResetPasswordResponse(GenericResponse):
  data: User



class BaseLocation(BaseModel):
  name: str
  address: str
  description: str | None = None
  phone: str | None = None
  longitude: float | None = None
  latitude: float | None = None
  radius: float | None = None
  is_active: bool = True
  updated_at: datetime | None = datetime.now()

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class UpdateLocation(BaseLocation):
  name: str | None = None
  address: str | None = None


class Location(BaseLocation):
  # _id: ObjectId | None = None
  # id: Any = Field(..., alias='_id')
  _id: str | None = None # mongo id
  id: str | None = None
  created_at: datetime | None = None
  updated_at: datetime | None = None
  attendance_history: List[AttendanceHistory] | None = []
  # users: User | None = None
  users: List[User] | None = []


class ListLocationResponse(BaseModel):
  status: str
  count: int
  data: List[Location]


class LocationResponse(BaseModel):
  status: str
  data: Location



class Settings(BaseModel):
  _id: str | None = None # mongo id
  id: str | None = None
  use_facial_recognition: bool = True
  use_qr_code: bool = True
  use_location: bool = False
  opens: str | None = "08:00"
  closes: str | None = "16:00"
  opening_window: int = 15  # in minutes
  closing_window: int = 15  # in minutes
  open_days: str | None = dumps(["mon", "tue", "wed", "thur", "fri"]) # json string
  is_active: bool = True
  created_at: datetime | None = datetime.now()
  updated_at: datetime | None = datetime.now()

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class ListSettingsResponse(BaseModel):
  status: str
  count: int
  data: List[Settings]


class SettingsResponse(BaseModel):
  status: str
  data: Settings
  message: str | None = None


class AttendanceHistoryWithUser(AttendanceHistory):
  user: User | None = None


class AttendanceHistoryResponseWithUser(AttendanceHistoryResponse):
  status: str
  data: AttendanceHistoryWithUser


class ListAttendanceHistoryResponseWithUser(ListAttendanceHistoryResponse):
  data: List[AttendanceHistoryWithUser]
