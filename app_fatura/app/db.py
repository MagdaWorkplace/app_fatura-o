import os.path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# Get the database directory of the file.
# os.path.join(__filename__) ensures correct path format.
# os.path.dirname(...) gets the folder containing this file.
BASE_DIR = os.path.dirname(os.path.join(__file__))

# SQLite #URL". -> SQLite database file path.
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"

# Create engine -> connection to the database.
# CONNECTION : FastAPI <-> SQLAchemy <-> SQLite database.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Session class -> temporary connection with the database.
# Each HTTP request, should have its own session.
session_local = sessionmaker(autocommit= False, autoflush= False, bind= engine)

# Base class for models. -> Keeps tracks of the database tables.
Base = declarative_base()

# Dependency to get DB session.
# Every request:
#  - creates a new database session.
#  - uses it
#  - closes the session after finishing the usage
def get_db():
    db = session_local() # Create a new session.
    try:
        yield db    # Give the session to the route.
    finally:
        db.close()  # Close the session.

# Function to create the database tables.
# If the tables already exist -> nothing happens.
def create_tables():
    # Looks at the information inherit from Base, checks if the tables exist in SQLite.
    # If nos -> creates them.
    Base.metadata.create_all(bind=engine)