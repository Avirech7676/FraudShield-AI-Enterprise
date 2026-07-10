from datetime import datetime, timedelta

from jose import jwt
from jose import JWTError

from app.config.settings import settings
from app.config.logging_config import logger


class JWTHandler:

    ###################################################

    @staticmethod
    def create_token(

        username,

        role

    ):

        expire = datetime.utcnow() + timedelta(

            minutes=settings.JWT_EXPIRE_MINUTES

        )

        payload = {

            "sub": username,

            "role": role,

            "exp": expire

        }

        token = jwt.encode(

            payload,

            settings.JWT_SECRET_KEY,

            algorithm=settings.JWT_ALGORITHM

        )

        logger.info(

            f"JWT Token Created for {username}"

        )

        return token

    ###################################################

    @staticmethod
    def verify_token(token):

        try:

            payload = jwt.decode(

                token,

                settings.JWT_SECRET_KEY,

                algorithms=[

                    settings.JWT_ALGORITHM

                ]

            )

            return payload

        except JWTError as e:

            logger.warning(

                f"JWT Verification Failed : {e}"

            )

            return None

        except Exception as e:

            logger.exception(

                f"Unexpected JWT Error : {e}"

            )

            return None