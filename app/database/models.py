from sqlmodel import SQLModel , Field , Relationship
from typing import Optional , List
from datetime import datetime , timezone

class User(SQLModel , table = True):
    user_id : str = Field(primary_key=True)
    username : str = Field(unique = True , index=True)
    email : str = Field(unique=True , index = True)
    hashed_password : str
    links : List["Link"] = Relationship(back_populates="user")

class Link(SQLModel , table = True):
    link_id: int | None = Field(primary_key=True)
    short_code : str = Field(unique=True , index = True)
    original_url : str 
    click_count : int = Field(default=0)
    user_id : Optional[str] = Field(default = None , foreign_key="user.user_id")
    created_at : datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    expired_at : Optional[datetime] | None = None
    user : Optional[User]  = Relationship(back_populates="links")
    
