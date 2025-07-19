from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    main_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
    main_phone_number: str
    user_name: str
    password: str
    type: str  # root | secondary
    name: str

    # Relaciones
    locations: List["Location"] = Relationship(back_populates="user")
    emergency_numbers: List["EmergencyNumber"] = Relationship(back_populates="user")
    sub_users: List["User"] = Relationship(back_populates="main_user", sa_relationship_kwargs={"foreign_keys": "[User.main_user_id]"})
    main_user: Optional["User"] = Relationship(back_populates="sub_users", sa_relationship_kwargs={"remote_side": "[User.id]"})
