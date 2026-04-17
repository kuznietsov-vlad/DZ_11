
from typing import Optional

from pydantic import EmailStr, BaseModel
from datetime import date

class Contact(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: date
    additional_info:str|None=None



class ContactResponse(Contact):
    id: int

    class Config:
        from_attributes = True


class ContactCreate(Contact):
    pass

class ContactUpdate(Contact):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birthday: Optional[str] = None
    additional_info: Optional[str] = None