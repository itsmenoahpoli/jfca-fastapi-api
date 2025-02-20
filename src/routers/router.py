from fastapi import FastAPI
from src.modules.auth.auth_controller import auth_router
from src.modules.user_roles.user_roles_controller import user_roles_router

def initialize_api_routes(app: FastAPI):
	app.include_router(auth_router)
	app.include_router(user_roles_router)