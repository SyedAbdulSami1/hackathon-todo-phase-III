from datetime import datetime
from typing import Optional, List, Union
from enum import Enum
from sqlmodel import SQLModel, Field, select
from pydantic import BaseModel, EmailStr, Field as PydanticField


# Base model for database tables
class BaseSQLModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Task Status Enum
class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# Database Models
class User(BaseSQLModel, table=True):
    __tablename__ = "users"

    username: str = Field(sa_column_kwargs={"unique": True}, index=True)
    email: EmailStr = Field(sa_column_kwargs={"unique": True}, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)


class Task(BaseSQLModel, table=True):
    __tablename__ = "tasks"

    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(max_length=1000, default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    user_id: int = Field(foreign_key="users.id", index=True)


# Pydantic Models for API
class TaskCreate(BaseModel):
    title: str = PydanticField(min_length=1, max_length=200)
    description: Optional[str] = PydanticField(max_length=1000, default=None)
    status: Optional[TaskStatus] = PydanticField(default=TaskStatus.PENDING)


class TaskUpdate(BaseModel):
    title: Optional[str] = PydanticField(min_length=1, max_length=200)
    description: Optional[str] = PydanticField(max_length=1000)
    status: Optional[TaskStatus]


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int


class TaskFilter(BaseModel):
    status: Optional[TaskStatus] = None
    search: Optional[str] = None


# Pydantic Models for API
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthResponse(BaseModel):
    user: UserResponse
    token: str
    token_type: str
