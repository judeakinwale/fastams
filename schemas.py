from datetime import datetime
from typing import List
from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    first_name: str
    last_name: str
    email: str
    hashed_password: str
    phone: str | None = None
    is_active: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListUserResponse(BaseModel):
    status: str
    count: int
    data: List[User]

