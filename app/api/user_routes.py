from fastapi import APIRouter
from fastapi import HTTPException

from app.database.connection import MongoDBConnection
from app.database.repository import FraudRepository

from app.auth.password_utils import PasswordManager

router = APIRouter()

db = MongoDBConnection().connect()

repository = FraudRepository(db)

@router.post("/users")
def add_user(user: dict):

    existing = repository.get_user(

        user["username"]

    )

    if existing:

        raise HTTPException(

            status_code=400,

            detail="User Already Exists"

        )

    user["password"] = PasswordManager.hash_password(

        user["password"]

    )

    repository.add_user(user)

    return {

        "status": "success"

    }
@router.put("/users/{username}/role")
def update_role(

    username: str,

    role: str

):

    repository.update_user_role(

        username,

        role

    )

    return {

        "status": "updated"

    }
@router.put("/users/{username}/password")
def reset_password(

    username: str,

    password: str

):

    password = PasswordManager.hash_password(

        password

    )

    repository.reset_password(

        username,

        password

    )

    return {

        "status": "updated"

    }
@router.delete("/users/{username}")
def delete_user(username: str):

    repository.delete_user(

        username

    )

    return {

        "status": "deleted"

    }