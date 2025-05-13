from src.database.entities import UserEntity
from src.utils.password_utils import hash_password

def seed_admin_user():
    existing_admin = UserEntity.find_one({"name": "Administrator Account"})
    
    if existing_admin:
        print("Admin user already exists")
        return
    
    hashed_password = hash_password('password')
    
    admin_user = {
        "name": "Administrator Account",
        "email": "admin@domain.com",
        "password": hashed_password,
        "user_type": "administrator",
        "is_enabled": True
    }
    
    UserEntity.insert_one(admin_user)
    print("Admin user created successfully")

if __name__ == "__main__":
    seed_admin_user() 