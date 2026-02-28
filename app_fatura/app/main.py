from fastapi import FastAPI
from routers.login import router as login_router
from routers.register import router as register_router
from routers import protected
from db import create_tables
# Create an instance of FastAPI.
app = FastAPI()

# Create database tables if they don't exist.
create_tables()

# Routes.
app.include_router(login_router)
app.include_router(register_router)
app.include_router(protected.router)


# Test if the serve works.
@app.get("/")
def root():
    # Retorna uma mensagem em formato JSON.
    return {"Hello": "Worlds"}
