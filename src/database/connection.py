from pymongo import mongo_client
from config.settings import app_settings

db_name = app_settings.app_database_db

db_client = mongo_client.MongoClient(
host=app_settings.app_database_url
)

def db_connect():
	try:
		server_info = db_client.server_info()
		print(server_info)

		if db_name not in db_client.list_database_names():
			db_database = db_client[db_name]

		return db_client[db_name]
	except Exception:
		print('Failed to connect to database')

def get_db_collection(collection: str, create_if_none: bool = False):
	db_database = db_connect()
	
	if not collection:
		raise ValueError("Collection must be a non-empty string")

	if create_if_none and collection not in db_database.list_collection_names():
		db_database.create_collection(collection)

	return db_database[collection]