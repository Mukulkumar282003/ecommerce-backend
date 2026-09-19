from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Query
from pathlib import Path
import shutil
from database import get_db
from utils.auth import get_current_user,require_admin
from schemas.product import ProductCreate,ProductResponse,ProductUpdate,ProductImageResponse
from schemas.common import MessageResponse
from services.product_service import (
    create_product,
    get_products as get_products_service,
    get_product as get_product_service,
    update_product as update_product_service,
    delete_product as delete_product_service
)    

router=APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("")
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category: str | None = None,
    search: str | None = None,
    sort: str | None = None,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_products_service(
        db,
        page,
        limit,
        category,
        search,
        sort
    )

@router.post("",response_model=ProductResponse)
def add_products(
    product_data:ProductCreate,
    db=Depends(get_db),
    current_user=Depends(require_admin)
):
    
    return create_product(db,product_data)

@router.get("/{product_id}",
response_model=ProductResponse)
def get_product(
    product_id:int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    product=get_product_service(db,product_id)
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    return product

@router.put("/{product_id}",
response_model=ProductResponse)
def update_product(
    product_id:int,
    product_data:ProductUpdate,
    db=Depends(get_db),
    current_user=Depends(require_admin)
):

    product=update_product_service(db,product_id,product_data)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="product not founnd"
        )
    return product

@router.delete("/{product_id}",response_model=MessageResponse)
def delete_product(
    product_id:int,
    db=Depends(get_db),
    current_user=Depends(require_admin)
):
    success=delete_product_service(db,product_id)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail="product not found"
        )
    return {
        "message":"product deleted successfully"
    }

@router.post("/{product_id}/image",response_model=ProductImageResponse)
async def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db=Depends(get_db),
    current_user=Depends(require_admin)
):
    product = get_product_service(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    allowed_extensions=[".jpg",".jpeg",".png",".webp"]

    file_extension=Path(image.filename).suffix.lower()

    if file_extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="only jpg,jpeg,png and webp images are allowed"
        )

    MAX_FILE_SIZE=5*1024*1024

    file_content=await image.read()

    if len(file_content)>MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="file size must be less than 5 MB"
        )

    image.file.seek(0)

    upload_folder = Path("uploads/products")

    upload_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = upload_folder / image.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    product.image_url = str(file_path)

    db.commit()
    db.refresh(product)

    return {
        "message": "Product image uploaded successfully",
        "image_url": product.image_url
    }

