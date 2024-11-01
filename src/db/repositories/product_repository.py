from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from src.db.models import Product
from src.schemas.product import ProductCreate, ProductUpdate, ProductOut


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate) -> ProductOut:
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return ProductOut.from_orm(db_product)

    def get_product_by_id(self, product_id: int) -> Optional[ProductOut]:
        try:
            db_product = self.db.query(Product).filter(Product.id == product_id).one()
            return ProductOut.from_orm(db_product)
        except NoResultFound:
            return None

    def get_all_products(self) -> List[ProductOut]:
        db_products = self.db.query(Product).all()
        return [ProductOut.from_orm(product) for product in db_products]

    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[ProductOut]:
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        for field, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product, field, value)
        self.db.commit()
        self.db.refresh(db_product)
        return ProductOut.from_orm(db_product)

    def delete_product_by_id(self, product_id: int) -> Optional[int]:
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
            return product_id
        return None
