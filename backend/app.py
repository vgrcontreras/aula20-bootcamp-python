from fastapi import FastAPI

from backend.routers import products

app = FastAPI()

app.include_router(products.router)

@app.get('/')
def read_root():
    return {'hello': 'world'}