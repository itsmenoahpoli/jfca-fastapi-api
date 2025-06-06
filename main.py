from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.routers.router import initialize_api_routes

app = FastAPI(
	title="JCFA API & Database",
	description="Main core data server",
	redoc_url=None
)

app.add_middleware(
  CORSMiddleware,
	allow_origins=['*'],
	allow_methods=["*"],
	allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory="public"), name="public")

initialize_api_routes(app)