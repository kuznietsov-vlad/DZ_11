# from wsgiref.validate import header_re

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from config.db import get_db
from src.auth.pass_utils import verify_password
from src.auth.repo import UserRepository
from src.auth.schema import UserResponse, UserCreate, Token
from src.auth.utils import create_access_token, create_refresh_token, decode_acces_token

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
        user_create: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered ")
    user = await user_repo.create_user(user_create)
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession     = Depends(get_db)
):
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    print(user.email)
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return Token(access_token= access_token, refresh_token= refresh_token, token_type= "bearer")


@router.post("/refresh", response_model=Token)
async def refresh_tokens(
        refresh_token: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    token_data=decode_acces_token(refresh_token)
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(refresh_token.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return Token(access_token= access_token, refresh_token= refresh_token, token_type= "bearer")





