import datetime
from pymongo.collection import Collection
from bson import ObjectId
from src.constants.errors_constant import ErrorTypes

class BaseRepository:
	def __init__(self, entity: Collection):
		self._entity = entity


	def _list_serializer(self, data: list):
		return [self._single_serializer(item) for item in data]

	def _single_serializer(self, data):
		if data:
			data["id"] = str(data["_id"])
			del data["_id"]
	
		return data
	
	def __check_if_exists(self, data, field_to_check):
		if len(self._list_serializer(self._entity.find({ field_to_check: data[field_to_check] }))) > 0:
			return True
		
		return False

	def get_list_data(self):
		result = self._entity.find()

		return self._list_serializer(result)

	def get_single_data(self, id):
		result = self._entity.find_one({ "_id": ObjectId(id) })

		if result == None:
			return ErrorTypes.NOT_FOUND_ERROR
		
		return self._single_serializer(result)

	def create_data(self, data, flag_unique_by = None):
		if flag_unique_by and self.__check_if_exists(data, flag_unique_by):
			return ErrorTypes.ALREADY_EXISTS

		data["createdAt"] = datetime.datetime.now(datetime.timezone.utc)
		data["updatedAt"] = datetime.datetime.now(datetime.timezone.utc)
		
		result = self._entity.insert_one(data)
		data["_id"] = str(result.inserted_id)
		
		return data

	def update_data(self, id, data):
		result = self._entity.update_one({ "_id": ObjectId(id) }, { "$set": data })

		if result.modified_count == 0:
			return None
		
		updated_data = self.get_single_data(id)

		return self._single_serializer(updated_data)
		


	def delete_data(self, id, is_soft_delete = False):
		if self.get_single_data(id) == ErrorTypes.NOT_FOUND_ERROR:
			return ErrorTypes.NOT_FOUND_ERROR
		
		if is_soft_delete:
			self.update_data(id, {
				"deletedAt": datetime.datetime.now(datetime.timezone.utc)
			})
		
		result = self._entity.delete_one({ "_id": ObjectId(id) })

		return result

		