import datetime
from pymongo.collection import Collection
from bson import ObjectId

class BaseRepository:
	def __init__(self, entity: Collection):
		self._entity = entity


	def __list_serializer(self, data: list):
		return [self.__single_serializer(item) for item in data]

	def __single_serializer(self, data: dict):
		if data:
			data["id"] = str(data["_id"])
			del data["_id"]
	
		return data
	
	def __check_if_exists(self, data: dict, field_to_check: str):
		if len(self.__list_serializer(self._entity.find({ field_to_check: data[field_to_check] }))) > 0:
			return True
		
		return False

	def get_list_data(self):
		result = self._entity.find()

		return self.__list_serializer(result)

	def get_single_data(self, id):
		result = self._entity.find_one({ "_id": ObjectId(id) })

		if result == None:
			return "NOT_FOUND"
		
		return self.__single_serializer(result)

	def create_data(self, data, flag_unique_by: str = None):
		if flag_unique_by and self.__check_if_exists(data, flag_unique_by):
			return 'ALREADY_EXIST'

		data["createdAt"] = datetime.datetime.now(datetime.timezone.utc)
		data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
		
		result = self._entity.insert_one(data)
		data["_id"] = str(result.inserted_id)
		
		return data

	def update_data(self, id: str, data: dict):
		result = self._entity.update_one({ "_id": ObjectId(id) }, { "$set": data })

		if result.modified_count == 0:
			return None
		
		updated_data = self.get_single_data(id)

		return self.__single_serializer(updated_data)
		


	def delete_data(self, id: str):
		if self.get_single_data(id) == "NOT_FOUND":
			return "NOT_FOUND"
		
		result = self._entity.delete_one({ "_id": ObjectId(id) })

		return result

		