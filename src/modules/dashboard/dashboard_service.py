from src.database.entities import UserRoleEntity, UserEntity, SectionEntity, StudentEntity

class DashboardService:
    def get_dashboard_counts(self):
        total_students = StudentEntity.count_documents({})
        total_sections = SectionEntity.count_documents({})
        total_user_roles = UserRoleEntity.count_documents({})
        total_users = UserEntity.count_documents({})
        
        return {
            "total_students": total_students,
            "total_sections": total_sections,
            "total_user_roles": total_user_roles,
            "total_users": total_users
        } 