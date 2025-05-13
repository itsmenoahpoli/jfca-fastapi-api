from .user_seeder import seed_admin_user

def run_all_seeders():
    print("Running database seeders...")
    seed_admin_user()
    print("All seeders completed!")

if __name__ == "__main__":
    run_all_seeders()