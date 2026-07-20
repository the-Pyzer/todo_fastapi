from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from models.shema import CreateUser,Token
from database import search_user,create_user
from auth.reglog import authenticate_user,create_access_token,timedelta,ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/register/',status_code=status.HTTP_201_CREATED)
def register(data: CreateUser,db: Session = Depends(get_db)):
    user = search_user(db,data)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Такой пользователь уже существует')
    new_user = create_user(db,data)
    return new_user

@router.post('/login/',status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Неверное имя пользователя или пароль")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user=user, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
