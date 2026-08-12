# Minimal security utilities for testing

def get_current_user(token: str | None = None):
    """Stub implementation used in tests.

    In the real application this would verify a JWT or session token and
    return the authenticated user record. For the purpose of unit tests we
    simply return a dummy user dictionary so that dependent services can
    operate without raising ``ImportError`` or ``AttributeError``.
    """
    # Return a minimal user representation expected by the services.
    return {
        "user_id": "test_user",
        "username": "test_user",
        "email": "test_user@example.com",
    }
