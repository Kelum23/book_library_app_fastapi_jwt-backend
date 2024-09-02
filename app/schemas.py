from pydantic import BaseModel
from typing import Optional
from datetime import date


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class BookBase(BaseModel):
    title: str
    author: str
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    cover_image: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str


class User(UserBase):
    id: int
    books: list[Book] = []

    class Config:
        orm_mode = True
