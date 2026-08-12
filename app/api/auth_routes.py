from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request

from app.auth.jwt_handler import JWTHandler
from app.auth.password_utils import PasswordManager
from app.auth.schemas import LoginRequest, RegisterRequest
from app.config.logging_config import logger
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
router = APIRouter(tags=["Authentication"])


@router.post("/register")
def register(payload: RegisterRequest, request: Request):
    repository = request.app.state.repository
    username = payload.username.strip()
    email = payload.email.strip()

    if repository.get_user(username):
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    if repository.get_user_by_email(email):
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    hashed_pw = PasswordManager.hash_password(payload.password)
    repository.add_user({
        "username": username,
        "email": email,
        "password": hashed_pw,
        "hashed_password": hashed_pw,
        "role": payload.role,
        "created_at": datetime.now(UTC)
    })

    return {
        "message": "User Registered Successfully"
    }


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
):
    repository = request.app.state.repository
    raw_username = form_data.username.strip() if form_data.username else ""

    user = repository.get_user(raw_username)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    stored_password_hash = user.get("password") or user.get("hashed_password")
    if not stored_password_hash or not PasswordManager.verify_password(
        form_data.password,
        stored_password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    matched_username = user.get("username", raw_username)
    matched_role = user.get("role", "Analyst")

    token = JWTHandler.create_token(
        matched_username,
        matched_role
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": matched_role
    }