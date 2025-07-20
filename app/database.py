from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL=os.getenv("postgresql://leo:CjdcVpoIUKHkbm2y4L8FbKyOhajPUTZG@dpg-d1u33gjuibrs7382f3i0-a:5432/panic_alarm_db")
engine= create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)