from datetime import datetime
from typing import List
from pydantic import BaseModel
from json import dumps


class GenericResponse(BaseModel):
  status: str
  data: dict | None = None
  message: str | None = None


class BaseAttendanceHistory(BaseModel):
  email: str
  user_id: int
  location_id: int | None = None
  image: str | None = None
  qr_code: str | None = None
  is_active: bool = True

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True

class AttendanceHistory(BaseAttendanceHistory):
  id: int | None = None
  # id: str | None = None
  phone: str | None = None
  # image: str | None = None
  image_encoding: str | None = None
  face_encoding: str | None = None
  # qr_code: str | None = None
  qr_code_content: str | None = None
  is_signed_in: bool = False
  is_signed_out: bool = False
  is_active: bool = True
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
  location_id: int | None = None
  is_admin: bool = False
  is_active: bool = True

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class CreateUser(BaseUser):
  password: str | None = None

class UpdateUser(CreateUser):
  first_name: str | None = None
  last_name: str | None = None
  email: str | None = None


class ResetPassword(BaseModel):
  password: str


class User(BaseUser):
  id: int | None = None
  # id: str | None = None
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

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class Location(BaseLocation):
  id: int | None = None
  # id: str | None = None
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
  use_facial_recognition: bool = True
  use_qr_code: bool = True
  use_location: bool = False
  opens: str = "8:00"
  closes: str = "16:00"
  open_days: str = dumps(["mon", "tue", "wed", "thur", "fri"]) # json string
  is_active: bool = True

  class Config:
    orm_mode = True
    allow_population_by_field_name = True
    arbitrary_types_allowed = True


class SettingsResponse(BaseModel):
  status: str
  data: Settings
  message: str | None = None


class AttendanceHistoryWithUser(AttendanceHistory):
  user: User


class AttendanceHistoryResponseWithUser(AttendanceHistoryResponse):
  status: str
  data: AttendanceHistoryWithUser


class ListAttendanceHistoryResponseWithUser(ListAttendanceHistoryResponse):
  data: List[AttendanceHistoryWithUser]
