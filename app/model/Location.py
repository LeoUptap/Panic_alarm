from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date, time

class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    lat : str
    long :str
    day: date
    time: time


