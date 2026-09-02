from fastapi import APIRouter
from fastapi import HTTPException

from app.api.auth_schemas import LoginRequest
from app.auth.jwt_handler import JWTHandler
from app.auth.password_utils import PasswordManager
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.config.logging_config import logger

router = APIRouter()

db = MongoDBConnection().connect()

repository = FraudRepository(db)

@router.post("/login")
def login(request: LoginRequest):

    user = repository.get_user(

        request.username

    )

    if user is None:

        logger.warning(

            f"Unknown user {request.username}"

        )

        raise HTTPException(

            status_code=401,

            detail="Invalid Username"

        )

    valid = PasswordManager.verify_password(

        request.password,

        user["password"]

    )

    if not valid:

        logger.warning(

            f"Wrong password {request.username}"

        )

        raise HTTPException(

            status_code=401,

            detail="Invalid Password"

        )

    token = JWTHandler.create_token(

        request.username,

        user["role"]

    )

    logger.info(
        
        f"{request.username} logged in"

    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "role": user["role"]

    }