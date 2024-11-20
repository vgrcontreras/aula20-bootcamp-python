from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, PositiveFloat


class Message(BaseModel):
    message: str

class ProductBase(BaseModel):
    name: str
    description: str
    price: PositiveFloat
    category: str
    supplier_email: EmailStr

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: str | None = None
    description: str | None = None
    price: PositiveFloat | None = None
    category: str | None = None
    supplier_email: EmailStr | None = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)