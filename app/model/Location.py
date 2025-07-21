from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, time
from model.User import User
class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    lat : str
    long :str
    day: date
    time: time

    user: Optional[User] = Relationship(back_populates="locations")
