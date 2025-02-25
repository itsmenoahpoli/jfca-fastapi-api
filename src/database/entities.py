from .connection import get_db_collection

# Users
UserRoleEntity = get_db_collection(collection='user_roles', create_if_none=True)
UserEntity = get_db_collection(collection='users', create_if_none=True)


# Sections and students
SectionEntity = get_db_collection(collection='sections', create_if_none=True)
StudentEntity = get_db_collection(collection='students', create_if_none=True)

# Logs
LogsUserSessionEntity = get_db_collection(collection='logs_user_sessions', create_if_none=True)
LogsSmsRecordsEntity = get_db_collection(collection='logs_sms_records', create_if_none=True)