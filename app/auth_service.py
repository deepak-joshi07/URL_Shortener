import os
import jwt
from sqlmodel import select , Session
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from datetime import timedelta , datetime , timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends , HTTPException , Request
from typing import Optional

from app.database.models import User
from app.id_generation.snowflake import id_generator
from app.security import hash_password , verify_password
from app.database.db import get_session

def create_user(username : str , email : str, password, session):
    existing_user = session.exec(
        select(User).where(
            User.username == username
        )
    ).first()

    if existing_user:
        raise ValueError("Username not available")

    existing_email = session.exec(
        select(User).where(
            User.email == email
        )
    ).first()

    if existing_email:
        raise ValueError("Email already in use")

    user_id = id_generator.generate_id()

    hashed_password = hash_password(password)

    user = User(
        user_id=user_id,
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=60) 
load_dotenv()  
SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def create_access_token(data:dict , expire_delta = ACCESS_TOKEN_EXPIRE_DELTA):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode.update({'exp':expire})

    encode_jwt = jwt.encode(to_encode ,SECRET_KEY , algorithm= ALGORITHM)

    return encode_jwt

def authenticate_user(identifier , password , session): 
        user = session.exec(
        select(User).where(
            (User.username == identifier) | (User.email == identifier)
        )
    ).first()

        if not user: 
            return False

        if not verify_password(password, user.hashed_password):
            return False


        return user
    

def login_user(identifier : str , password , session):

    user = authenticate_user(identifier , password , session)

    if not user:
         raise ValueError("Invalid credentials")

    token = create_access_token(
         {"sub" : str(user.user_id)}
    )

    return token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl= "/login"
)

def decode_access_token(token : str): 
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY , 
            algorithms= [ALGORITHM]
        )

        return payload
    except InvalidTokenError:
        return None
    
def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    try:
        user_id = int(user_id)
    except (TypeError , ValueError):
        raise HTTPException(
            status_code= 401 , 
            detail= 'Invalid token payload'
        )

    user = session.exec(
        select(User)
        .where(User.user_id == user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


def get_optional_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> Optional[User]:
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return None 
    
    token = auth_header.split(" ")[1]
    
    try:
        payload = decode_access_token(token)  

        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        user = session.get(User, int(user_id))
        return user
    except Exception:
        return None  

    