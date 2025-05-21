from .user_seeder import seed_admin_user
from .student_key_seeder import seed_student_keys

def run_all_seeders():
    print("Running database seeders...")
    seed_admin_user()
    seed_student_keys()
    print("All seeders completed!")

if __name__ == "__main__":
    run_all_seeders()