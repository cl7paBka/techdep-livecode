from src.api.cart_routes import cart_api_router
from src.api.people_routes import people_api_router
from src.api.product_routes import product_api_router

#This is an API package
routers = (cart_api_router, people_api_router, product_api_router)
