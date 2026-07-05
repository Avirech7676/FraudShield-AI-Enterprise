from app.auth.password_utils import PasswordManager
from app.database.connection import MongoDBConnection

db = MongoDBConnection().connect()

users = list(

    db.users.find()

)

for user in users:

    if user["password"].startswith("$2"):

        continue

    hashed = PasswordManager.hash_password(

        user["password"]

    )

    db.users.update_one(

        {

            "_id": user["_id"]

        },

        {

            "$set": {

                "password": hashed

            }

        }

    )

print("Users Updated")