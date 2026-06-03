from pydantic import BaseModel
from datetime import date
from typing import Optional

# Category schemas
class CategoryBase(BaseModel):
    name: str
    budget_limit: float

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    budget_limit: float

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# Subcategory schemas
class SubcategoryBase(BaseModel):
    name: str
    category_id: int

class SubcategoryCreate(SubcategoryBase):
    pass

class SubcategoryUpdate(BaseModel):
    name: str

class SubcategoryResponse(SubcategoryBase):
    id: int
    total_spent: float = 0.0

    class Config:
        from_attributes = True


# Transaction schemas
class TransactionBase(BaseModel):
    amount: float
    date: date
    subcategory_id: int

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int

    class Config:
        from_attributes = True