from app.database.connection import MongoDBConnection


def test_database_connection():

    db = MongoDBConnection().connect()

    assert db is not None