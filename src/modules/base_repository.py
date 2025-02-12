class BaseRepository():
	def __init__(self, entity):
		self._entity = entity

		print('BaseRepository initialized')