from fastapi import FastAPI
from src.modules.auth.auth_controller import auth_router

def initialize_api_routes(app: FastAPI):
	app.include_router(auth_router)