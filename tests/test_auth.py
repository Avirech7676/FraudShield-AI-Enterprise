from app.auth.jwt_handler import JWTHandler


def test_token():

    token = JWTHandler.create_token(

        "admin",

        "Admin"

    )

    payload = JWTHandler.verify_token(

        token

    )

    assert payload["sub"] == "admin"

    assert payload["role"] == "Admin"