from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth.jwt_handler import JWTHandler

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

#####################################################

@router.get("")
def get_users(

    request: Request,

    user=Depends(JWTHandler.verify_token)

):
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    if user.get("role") != "Admin":

        raise HTTPException(

            status_code=403,

            detail="Admin Access Required"

        )

    return request.app.state.repository.get_all_users()

#####################################################

@router.delete("/{username}")

def delete_user(

    username: str,

    request: Request,

    user=Depends(JWTHandler.verify_token)

):
    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    if user.get("role") != "Admin":

        raise HTTPException(

            status_code=403,

            detail="Admin Access Required"

        )

    result = request.app.state.repository.delete_user(

        username

    )

    if result.deleted_count == 0:

        raise HTTPException(

            status_code=404,

            detail="User Not Found"

        )

    return {

        "message": "User Deleted Successfully"

    }

#####################################################

@router.patch("/{username}/role")

def update_role(

    username: str,

    role: str,

    request: Request,

    user=Depends(JWTHandler.verify_token)

):
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    if user.get("role") != "Admin":

        raise HTTPException(

            status_code=403,

            detail="Admin Access Required"

        )

    request.app.state.repository.update_user_role(

        username,

        role

    )

    return {

        "message": "Role Updated"

    }