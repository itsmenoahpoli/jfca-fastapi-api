from fastapi import FastAPI
from src.modules.auth.auth_controller import auth_router
from src.modules.user_roles.user_roles_controller import user_roles_router
from src.modules.sections.sections_controller import sections_router
from src.modules.students.students_controller import students_router
from src.modules.notifications.notifications_controller import notifications_router
from src.modules.dashboard.dashboard_controller import dashboard_router
from src.modules.attendance.attendance_controller import attendance_router
from src.modules.users.users_controller import users_router
from src.modules.face_recognition.face_recognition_controller import router as face_recognition_router

API_PREFIX_V1 = "/api/v1"

app_routers = [
    auth_router,
    user_roles_router,
    sections_router,
    students_router,
    notifications_router,
    dashboard_router,
    attendance_router,
    users_router,
    face_recognition_router
]

def initialize_api_routes(app: FastAPI):
    for router in app_routers:
        app.include_router(router=router, prefix=API_PREFIX_V1)