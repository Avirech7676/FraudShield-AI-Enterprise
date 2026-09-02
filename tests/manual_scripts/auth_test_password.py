from app.auth.password_utils import PasswordManager

password = "admin123"

hashed = PasswordManager.hash_password(password)

print("Original :", password)

print("Hashed :", hashed)

print()

print(

    PasswordManager.verify_password(

        password,

        hashed

    )

)