from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.db.repositories.cart_repository import CartRepository
from src.schemas.cart import CartCreate, CartOut, CartItemCreate, CartItemOut
from src.db import get_db

cart_api_router = APIRouter(prefix="/cart")


@cart_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
def create_cart(cart: CartCreate, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    created_cart = cart_repo.create_cart(cart)
    return {
        "status": "success",
        "message": f"Cart with ID {created_cart.id} created successfully.",
        "data": created_cart.dict()
    }


@cart_api_router.get("/{cart_id}", response_model=Dict)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    cart = cart_repo.get_cart_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {
        "status": "success",
        "message": f"Cart with ID {cart_id} retrieved successfully.",
        "data": cart.dict()
    }


@cart_api_router.post("/{cart_id}/items/add", response_model=Dict, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(cart_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    added_item = cart_repo.add_item_to_cart(cart_id, item)
    return {
        "status": "success",
        "message": f"Item added to cart with ID {cart_id} successfully.",
        "data": added_item.dict()
    }


@cart_api_router.get("/{cart_id}/items", response_model=Dict)
def get_all_cart_items(cart_id: int, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    items = cart_repo.get_all_cart_items(cart_id)
    return {
        "status": "success",
        "message": f"All items in cart with ID {cart_id} retrieved successfully.",
        "data": [item.dict() for item in items]
    }


@cart_api_router.delete("/delete/{cart_id}", response_model=Optional[Dict])
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    deleted_cart_id = cart_repo.delete_cart(cart_id)
    if not deleted_cart_id:
        raise HTTPException(status_code=404, detail="Cart not found")
    return {
        "status": "success",
        "message": f"Cart with ID {cart_id} deleted successfully.",
        "data": None
    }


@cart_api_router.delete("/items/delete/{item_id}", response_model=Optional[Dict])
def delete_cart_item(item_id: int, db: Session = Depends(get_db)):
    cart_repo = CartRepository(db)
    deleted_item_id = cart_repo.delete_cart_item(item_id)
    if not deleted_item_id:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {
        "status": "success",
        "message": f"Cart item with ID {item_id} deleted successfully.",
        "data": None
    }
