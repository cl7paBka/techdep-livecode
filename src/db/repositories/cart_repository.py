from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from src.db.models import Cart, CartItems
from src.schemas.cart import CartCreate, CartOut, CartItemCreate, CartItemOut


class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_cart(self, cart: CartCreate) -> CartOut:
        db_cart = Cart(user_id=cart.user_id)
        self.db.add(db_cart)
        self.db.commit()
        self.db.refresh(db_cart)
        return CartOut.from_orm(db_cart)

    def get_cart_by_id(self, cart_id: int) -> Optional[CartOut]:
        try:
            db_cart = self.db.query(Cart).filter(Cart.id == cart_id).one()
            return CartOut.from_orm(db_cart)
        except NoResultFound:
            return None

    def add_item_to_cart(self, cart_id: int, item: CartItemCreate) -> CartItemOut:
        db_item = CartItems(cart_id=cart_id, **item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return CartItemOut.from_orm(db_item)

    def get_all_cart_items(self, cart_id: int) -> List[CartItemOut]:
        db_items = self.db.query(CartItems).filter(CartItems.cart_id == cart_id).all()
        return [CartItemOut.from_orm(item) for item in db_items]

    def delete_cart_item(self, item_id: int) -> Optional[int]:
        db_item = self.db.query(CartItems).filter(CartItems.id == item_id).first()
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return item_id
        return None

    def delete_cart(self, cart_id: int) -> Optional[int]:
        db_cart = self.db.query(Cart).filter(Cart.id == cart_id).first()
        if db_cart:
            self.db.delete(db_cart)
            self.db.commit()
            return cart_id
        return None
