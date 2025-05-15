from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from src.modules.base_repository import BaseRepository
from src.modules.attendance.models import AttendanceEntry

class AttendanceRepository(BaseRepository):
    def __init__(self):
        super().__init__("attendance_entries")

    async def create(self, attendance: AttendanceEntry) -> AttendanceEntry:
        attendance_dict = attendance.dict()
        attendance_dict["created_at"] = datetime.utcnow()
        attendance_dict["updated_at"] = datetime.utcnow()
        result = await self.collection.insert_one(attendance_dict)
        attendance_dict["_id"] = result.inserted_id
        return AttendanceEntry(**attendance_dict)

    async def get_by_id(self, attendance_id: str) -> Optional[AttendanceEntry]:
        result = await self.collection.find_one({"_id": ObjectId(attendance_id)})
        return AttendanceEntry(**result) if result else None

    async def get_by_student_id(self, student_id: str) -> List[AttendanceEntry]:
        cursor = self.collection.find({"student_id": ObjectId(student_id)})
        return [AttendanceEntry(**doc) async for doc in cursor]

    async def update(self, attendance_id: str, attendance: AttendanceEntry) -> Optional[AttendanceEntry]:
        attendance_dict = attendance.dict()
        attendance_dict["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": ObjectId(attendance_id)},
            {"$set": attendance_dict}
        )
        if result.modified_count:
            return await self.get_by_id(attendance_id)
        return None

    async def delete(self, attendance_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(attendance_id)})
        return result.deleted_count > 0 