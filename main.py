from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from fastapi.staticfiles import StaticFiles
from utils.logger import logger
from utils.config import APP_NAME,APP_VERSION
from routers.product import router as product_router
from routers.user import router as user_router
from routers.cart import router as cart_router
from routers.order import router as order_router


app=FastAPI(
    title=APP_NAME,
    description="Production-style E-commmerce backend API",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    logger.info("E-Commerce API started successfully")


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database error",
            "message": "Something went wrong with the database"
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong"
        }
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

@app.get("/health",tags=["Health"]) 
def health_check():
    return {
        "status":"healthy",
        "service":"E-commerce API"
    }


