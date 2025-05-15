from typing import List, Optional
from src.modules.attendance.models import AttendanceEntry
from src.modules.attendance.repository import AttendanceRepository

class AttendanceService:
    def __init__(self):
        self.repository = AttendanceRepository()

    async def create_attendance(self, attendance: AttendanceEntry) -> AttendanceEntry:
        return await self.repository.create(attendance)

    async def get_attendance(self, attendance_id: str) -> Optional[AttendanceEntry]:
        return await self.repository.get_by_id(attendance_id)

    async def get_student_attendance(self, student_id: str) -> List[AttendanceEntry]:
        return await self.repository.get_by_student_id(student_id)

    async def update_attendance(self, attendance_id: str, attendance: AttendanceEntry) -> Optional[AttendanceEntry]:
        return await self.repository.update(attendance_id, attendance)

    async def delete_attendance(self, attendance_id: str) -> bool:
        return await self.repository.delete(attendance_id) 