from pydantic import BaseModel , EmailStr , HttpUrl
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username : str
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str
class UserResponse(BaseModel): 
    user_id : str
    username : str
    email : EmailStr
class LinkCreate(BaseModel): 
    original_url : HttpUrl
    custom_alias : Optional[str] = None
    expires_at : Optional[datetime] = None
class LinkUpdate(BaseModel): 
    original_url : Optional[HttpUrl]
    expires_at : Optional[datetime]

class LinkResponse(BaseModel): 
    short_code : str
    short_url : str
    original_url : HttpUrl
    click_count : int 
    created_at : datetime
    expires_at : Optional[datetime] = None


class TokenResponse(BaseModel): 
    access_token : str
    refresh_token : str
    token_type : str = 'bearer'