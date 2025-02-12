from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.router import initialize_api_routes

app = FastAPI(
	title="JFCA API",
	description="Main core data server",
	contact={
		"name": "@itznoahdev"
	}
)

app.add_middleware(
  CORSMiddleware,
	allow_origins=['*'],
	allow_methods=["*"],
	allow_headers=["*"],
)

initialize_api_routes(app)

@app.get('/')
def index():
	return "SYSTEM_ONLINE"