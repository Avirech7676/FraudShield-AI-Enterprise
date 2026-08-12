from app.auth.users import USERS


class AuthenticationManager:

    def authenticate(
        self,
        username,
        password
    ):

        if username not in USERS:

            return False, None

        user = USERS[username]

        if user["password"] == password:

            return True, user["role"]

        return False, None
