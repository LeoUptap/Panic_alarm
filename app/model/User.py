from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from model.Emergency_number import Emergency_number
from model.Location import Location
from sqlalchemy.orm import Mapped


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    main_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    main_phone_number: str
    user_name: str = Field(unique=True, nullable=False)
    password: str
    type: str  # root | secondary
    name: str

    # Relaciones
    emergency_numbers: Mapped[List["Emergency_number"]] = Relationship()


    locations: Mapped[List["Location"]] = Relationship()
    sub_users: Mapped[List["User"]] = Relationship(
        back_populates="main_user",
        sa_relationship_kwargs={"foreign_keys": "User.main_user_id"}
    )
    main_user: Mapped[Optional["User"]] = Relationship(
        back_populates="sub_users",
        sa_relationship_kwargs={"remote_side": "User.id"}
    )
