from app.auth.jwt_handler import JWTHandler

token = JWTHandler.create_token(

    "admin",

    "Admin"

)

print("Token")

print(token)

print()

print("Decoded")

print(

    JWTHandler.verify_token(

        token

    )

)