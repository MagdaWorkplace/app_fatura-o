from fastapi import FastAPI
from routers.login import router as login_router
from routers.register import router as register_router
from routers import protected
from db import create_tables
from routers.upload_invoice import router as upload_invoice
from routers.invoices import router as invoices
from fastapi.middleware.cors import CORSMiddleware


# Create an instance of FastAPI.
app = FastAPI()

# Create database tables if they don't exist.
create_tables()

# Enable CORS for your frontend -> Enable frontend to do requests.
origins = [
    "http://localhost:5173",  # React dev server.
    "http://127.0.0.1:5173"
]

# Add CORS middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Allow frontend.
    allow_credentials=True,
    allow_methods=["*"],         # Allow methods like: POST, GET, OPTIONS, etc.
    allow_headers=["*"],         # Allow headers like Content-Type.
)


# Routes.
app.include_router(login_router)
app.include_router(register_router)
app.include_router(protected.router)
app.include_router(upload_invoice)
app.include_router(invoices)

# Test if the serve works.
@app.get("/")
def root():
    # Retorna uma mensagem em formato JSON.
    return {"Hello": "Worlds"}
