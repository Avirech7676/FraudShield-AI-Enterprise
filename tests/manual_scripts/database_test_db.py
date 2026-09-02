from app.database.connection import MongoDBConnection


def main():

    db = MongoDBConnection()

    database = db.connect()

    print()

    print("Database Name :")

    print(database.name)

    print()

    db.close()


if __name__ == "__main__":

    main()