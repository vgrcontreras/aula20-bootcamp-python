from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import Product
from backend.schemas import ProductCreate, ProductResponse

router = APIRouter(prefix='/products', tags=['products'])


@router.post('/', response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_session),
):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

@router.get('/', response_model=List[ProductResponse])
def read_all_products(session: Session = Depends(get_session)):
    products_db = session.scalars(
        select(Product)
    ).all()
    
    return products_db

