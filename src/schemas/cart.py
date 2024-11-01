from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass


class CartItemOut(CartItemBase):
    id: int
    cart_id: int
    added_at: datetime

    class Config:
        orm_mode = True


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    items: List[CartItemCreate] = []


class CartOut(CartBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[CartItemOut] = []

    class Config:
        from_attributes = True


class CartCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CartUpdate(BaseModel):
    quantity: Optional[int] = None

    class Config:
        from_attributes = True


class CartInfo(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
