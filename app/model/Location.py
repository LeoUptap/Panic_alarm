from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date, time
from sqlalchemy.orm import Mapped

class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    lat : str
    long :str
    day: date
    time: time

    user: Mapped[Optional["User"]] = Relationship(back_populates="locations")

