from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.product import router as product_router
from routers.user import router as user_router
from routers.cart import router as cart_router
from routers.order import router as order_router


app=FastAPI(
    title="E-commerce API",
    version="1.0,0"   
)

app.mount("/uploads",
          StaticFiles(directory="uploads"),
          name="uploads"
)

app.include_router(product_router)
app.include_router(user_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.get("/")
def home ():
    return{"message":"E-commerce API is running"}
