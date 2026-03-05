from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

# Model for JSON body of the post request.

class RequestRegister(BaseModel):
    username: str
    password: str = Field(max_length=72, description="The password need to be 72 charcters or less.")


class RequestLogin(BaseModel):
    username: str
    password: str


class User(Base):
    # Name of the table in SQLite.
    __tablename__ = "users"
    # Primary key column (Unique ID)
    id = Column(Integer, primary_key=True,index=True)
    # Username column.
    username= Column(String, unique=True, index=True, nullable=False)
    # Hashed password column.
    hashed_password = Column(String, nullable=False)


class Invoice(Base):
    # Name of the table in SQLite.
    __tablename__ = "invoices"

    # Primary key column (Unique ID)
    id = Column(Integer, primary_key=True, index=True)
    # Link the invoice to the specific user.
    user_id = Column(Integer, ForeignKey("users.id"))
    # QR data - raw information, decoded string.
    qr_raw_data = Column(String, nullable=False)
    # Parsed fields -> add more later.
    invoice_number = Column(String)
    total_amount = Column(String)
    date = Column(String)