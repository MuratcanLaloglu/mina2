from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class InputData(BaseModel):
    married: float
    income: float
    education: float
    loan_amount: float
    credit_history: float


class Functions(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    model1: bool = Field(default=False)
    model2: bool = Field(default=False)
    model3: bool = Field(default=False)
    credits: int = Field(default=0)

class CommercialCustomer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_name: str
    contact_person_first_name: str
    contact_person_last_name: str
    contact_person_position: str
    address_street: str
    address_city: str
    address_state: str
    address_zip_code: str
    address_country: str
    phone_number: str
    email: str
    website: str
    tax_id: str
    business_type: str


class PersonalCustomer(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_street: str
    address_city: str
    address_state: str
    address_zip_code: str
    address_country: str
    phone_number: str
    email: str
    date_of_birth: str
    gender: str
    occupation: str


class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_name: str
    description: str
    start_date: str
    end_date: str
    budget: float
    client_company_name: str
    client_contact_person_first_name: str
    client_contact_person_last_name: str
    client_contact_person_position: str
    client_phone_number: str
    client_email: str
    status: str


class Employee(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    address_street: str
    address_city: str
    address_state: str
    address_zip_code: str
    address_country: str
    phone_number: str
    email: str
    date_of_birth: str
    gender: str
    position: str
    department: str
    salary: float
    date_hired: str


class Competitor(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_name: str
    address_street: str
    address_city: str
    address_state: str
    address_zip_code: str
    address_country: str
    phone_number: str
    email: str
    website: str
    industry: str
    number_of_employees: int
    annual_revenue: float
