from __future__ import annotations
from sqlmodel import SQLModel, Field
from typing import Optional


class Emergency_number(SQLModel, table=True):
    id:int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    phone_number: str
    name: str
