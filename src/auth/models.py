from pygments.lexer import default
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import roles
from sqlalchemy.testing.schema import mapped_column

from config.db import Base
from src.contacts.schema import Contact

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True)

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True ,index=True)
    email: Mapped[str] = mapped_column(String, unique=True ,index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(default=True)
    contacts: Mapped[list[Contact]] = relationship("Contact", back_populates="owner")
    role_id:Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=True)
    role: Mapped[str] = relationship("Role", lazy="selectin")



