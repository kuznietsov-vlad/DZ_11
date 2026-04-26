
from datetime import date, timedelta

from dns.e164 import query
from pydantic.v1 import EmailStr
from sqlalchemy import select

from src.contacts.models import Contact
from src.contacts.schema import ContactCreate, ContactUpdate


class ContactRepository:
    def __init__(self, session):
        self.session = session

    async def get_contact(self, contact_id: int) -> Contact:

        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_contact(self, contact: ContactCreate, owner_id: int) -> Contact:
        new_contact = Contact(**contact.model_dump(), owner_id= owner_id  )
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)
        return new_contact

    async def update_contact(self, contact: ContactUpdate, contact_id: int) -> Contact:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        db_contact = result.scalar_one_or_none()
        if not db_contact:
            return None

        updated_contact = contact.model_dump(exclude_unset=True)
        for key, value in updated_contact.items():
            setattr(db_contact, key, value)
        await self.session.commit()
        await self.session.refresh(db_contact)

        return db_contact

    async def delete_contact(self, contact_id: int) -> bool:
        query = select(Contact).where(Contact.id == contact_id)
        result = await self.session.execute(query)
        db_contact = result.scalar_one_or_none()
        if not db_contact:
            return False
        await self.session.delete(db_contact)
        await self.session.commit()
        return True

    async def get_all_contacts(self, owner_id, skip:int = 0, limit: int =10):
        query = select(Contact).where(Contact.owner_id == owner_id).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_contact(self, first_name: str = None, last_name: str = None, email: EmailStr = None):
        query = select(Contact)
        if first_name:
            query = query.where(Contact.first_name == first_name)
        if last_name:
            query = query.where(Contact.last_name == last_name)
        if email:
            query = query.where(Contact.email == email)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_birthdays(self):
        today= date.today()
        end_date= today + timedelta(days=7)
        result = await self.session.execute(select(Contact))
        contacts =result.scalars().all()
        upcoming_bdays = []
        for contact in contacts:
            bday = contact.birthday.replace(year=today.year)
            if today <= bday <= end_date:
                upcoming_bdays.append(contact)
        return upcoming_bdays
