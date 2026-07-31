from sqlmodel import create_engine , Session
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None: 
    raise ValueError("DATABASE_URL environment variable is missing.")

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

