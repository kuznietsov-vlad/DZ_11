from fastapi import APIRouter, Query, Path, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.db import get_db
from src.auth.models import User
from src.auth.schema import RoleEnum
from src.auth.utils import get_current_user, RoleChecker
from src.contacts.repos import ContactRepository
from src.contacts.schema import ContactResponse, Contact, ContactCreate, ContactUpdate
from typing import Optional
router = APIRouter()


# @router.get("/contact/all")
# async def get_contact_all(skip: int = None, limit: int = Query(default =10,le=100,ge=10)):
#     return {"contacts": f"all contacts, skip = {skip}, limit = {limit}"}
#
#
#@router.post("/contact")
# async def create_contact(contact:Contact) -> ContactResponse:
#     return ContactResponse(first_name=contact.first_name, last_name=contact.last_name)


@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate,
                         db: AsyncSession = Depends(get_db),
                         user: User = Depends(get_current_user)
                         ):
    contact_repo = ContactRepository(db)
    new_contact = await contact_repo.create_contact(contact, user.id)

    return new_contact


@router.get("/search", response_model=List[ContactResponse])
async def find_contacts(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    email: Optional[EmailStr] = None,
    db: AsyncSession = Depends(get_db)
    ):
    contact_repo = ContactRepository(db)
    contacts = await contact_repo.find_contact(first_name, last_name, email)
    return contacts

@router.get("/", response_model=List[ContactResponse])
async def get_all_contacts(
        skip: int = 0,
        limit: int = 10,
        user: User = Depends(RoleChecker([RoleEnum.USER])),
        db: AsyncSession = Depends(get_db)
):

    repo = ContactRepository(db)
    return await repo.get_all_contacts(user.id, skip, limit)



@router.get("/birthdays", response_model=List[ContactResponse])
async def find_birthdays( db: AsyncSession = Depends(get_db)):
    repo = ContactRepository(db)
    return await repo.get_birthdays()


@router.patch("/{contact_id}", response_model=List[ContactResponse])
async def update_contact(contact_id: int, data: ContactUpdate, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact = await contact_repo.update_contact(data, contact_id)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact

@router.delete("/{contact_id}")
async def delete_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact_repo = ContactRepository(db)
    contact_for_delete = await contact_repo.delete_contact(contact_id)
    if not contact_for_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
