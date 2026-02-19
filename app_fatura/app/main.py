from fastapi import FastAPI
from routers.login import router as login_router
# Create an instance of FastAPI.
app = FastAPI()


# Routes.
app.include_router(login_router)


# Test if the serve works.
@app.get("/")
def root():
    # Retorna uma mensagem em formato JSON.
    return{"Hello":"Worlds"}

