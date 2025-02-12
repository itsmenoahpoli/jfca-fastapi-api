from .connection import get_db_collection

UserEntity = get_db_collection(collection='users', create_if_none=True)