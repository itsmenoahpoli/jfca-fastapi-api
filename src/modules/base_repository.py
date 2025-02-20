from pymongo.collection import Collection
class BaseRepository:
	def __init__(self, entity: Collection):
		self._entity = entity


	@staticmethod
	def __list_serializer(data: list):
		return [{**item, "id": str(item["_id"])} for item in data]

	@staticmethod
	def __single_serializer(data: dict):
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

	def get_single_data(self):
		pass

	def create_data(self, data, flag_unique_by: str = None):
		print()
		if flag_unique_by and self.__check_if_exists(data, flag_unique_by):
			return 'ALREADY_EXIST'

		result = self._entity.insert_one(data)
		data["_id"] = str(result.inserted_id)
		
		return data

	def update_data(self):
		pass

	def delete_data(self):
		pass