from jose import JWTError
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from dependencies import get_db
from models.models import User
import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 3600))

oath2 = OAuth2PasswordBearer(tokenUrl='/login')

password_hash = PasswordHash.recommended()
FAKE_PASSWORD = password_hash.hash('kplasfkasdmam,fa')

def hashed_password(password: str):
    return password_hash.hash(password)

def verify_password(plain_password: str,password: str):
    return password_hash.verify(plain_password,password)

def find_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user

def find_user_name(db: Session, name: str):
    user = db.query(User).filter(User.name == name).first()
    return user

def authenticate_user(db: Session, name: str, password: str):
    user = find_user_name(db, name)
    if not user:
        verify_password(password, FAKE_PASSWORD)
        return False
    if not verify_password(password, user.password):
        return False

    return user

def create_access_token(user: User, expires_delta: timedelta | None = None):

    to_encode = {
        'sub': str(user.id),
        'name': user.name
    }

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token

def get_current_user(token: str = Depends(oath2),db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = find_user(db,int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


