from fastapi import HTTPException

class Roles:

    @staticmethod
    def require(role):

        def checker(user):

            if user["role"] != role:

                raise HTTPException(
                    status_code=403,
                    detail="Permission Denied"
                )

            return user

        return checker
    