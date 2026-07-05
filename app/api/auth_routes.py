from fastapi import APIRouter
from fastapi import HTTPException

from app.api.auth_schemas import LoginRequest
from app.auth.jwt_handler import JWTHandler
from app.auth.password_utils import PasswordManager
from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository
from app.logging.logger import EnterpriseLogger

router = APIRouter()

db = MongoDBConnection().connect()

repository = FraudRepository(db)

@router.post("/login")
def login(request: LoginRequest):

    user = repository.get_user(

        request.username

    )

    if user is None:

        EnterpriseLogger.warning(

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

        EnterpriseLogger.warning(

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

    EnterpriseLogger.info(

        f"{request.username} logged in"

    )

    return {

        "access_token": token,

        "token_type": "bearer",

        "role": user["role"]

    }