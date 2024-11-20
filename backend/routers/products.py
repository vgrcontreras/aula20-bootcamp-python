from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.database import get_session
from backend.models import Product
from backend.schemas import (Message, ProductCreate, ProductResponse,
                             ProductUpdate)

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
def read_all_products(db: Session = Depends(get_session)):
    products_db = db.scalars(
        select(Product)
    ).all()

    return products_db


@router.get('/{product_id}', response_model=ProductResponse)
def read_product(
    product_id: int,
    db: Session = Depends(get_session)
):
    product_db = db.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado'
        )
    
    return product_db


@router.delete('/{product_id}', response_model=Message)
def delete_product(
    product_id: int,
    db: Session = Depends(get_session)
):
    product_db = db.scalar(
    select(Product).where(Product.id == product_id)
    )

    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Produto não encontrado'
        )
    
    db.delete(product_db)
    db.commit()

    return {'message': 'Product deleted successfully'}


@router.patch('/{product_id}', response_model=ProductResponse)
def patch_todo(
    product_id: int,
    product: ProductUpdate,
    session: Session = Depends(get_session),
):
    product_db = session.scalar(
        select(Product).where(Product.id == product_id)
    )

    if not product_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(product_db, key, value)

    session.add(product_db)
    session.commit()
    session.refresh(product_db)

    return product_db