from .connection import get_db_collection

UserRole = get_db_collection(collection='user_roles', create_if_none=True)