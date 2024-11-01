from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Optional
from sqlalchemy.orm import Session
from src.db.repositories.product_repository import ProductRepository
from src.schemas.product import ProductCreate, ProductUpdate, ProductOut
from src.db import get_db

product_api_router = APIRouter(prefix="/product")


@product_api_router.post("/create", response_model=Dict, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    created_product = product_repo.create_product(product)
    return {
        "status": "success",
        "message": f"Product with ID {created_product.id} created successfully.",
        "data": created_product.dict()
    }


@product_api_router.get("/{product_id}", response_model=Dict)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    product = product_repo.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "success",
        "message": f"Product with ID {product_id} retrieved successfully.",
        "data": product.dict()
    }


@product_api_router.get("/", response_model=Dict)
def get_all_products(db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    products = product_repo.get_all_products()
    return {
        "status": "success",
        "message": "All products retrieved successfully.",
        "data": [product.dict() for product in products]
    }


@product_api_router.patch("/update/{product_id}", response_model=Dict)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    updated_product = product_repo.update_product(product_id, product_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "success",
        "message": f"Product with ID {product_id} updated successfully.",
        "data": updated_product.dict()
    }


@product_api_router.delete("/delete/{product_id}", response_model=Optional[Dict])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_repo = ProductRepository(db)
    deleted_product_id = product_repo.delete_product_by_id(product_id)
    if not deleted_product_id:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "status": "success",
        "message": f"Product with ID {product_id} deleted successfully."
    }
