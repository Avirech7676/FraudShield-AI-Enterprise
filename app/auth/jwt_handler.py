import os

from datetime import datetime, timedelta

from jose import jwt
from jose import JWTError

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
EXPIRE_MINUTES = int(
    os.getenv("JWT_EXPIRE_MINUTES", 60)
)


class JWTHandler:

    @staticmethod
    def create_token(username, role):

        expire = datetime.utcnow() + timedelta(
            minutes=EXPIRE_MINUTES
        )

        payload = {
            "sub": username,
            "role": role,
            "exp": expire
        }

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def verify_token(token):

        try:

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            return payload

        except JWTError:

            return None