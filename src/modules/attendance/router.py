from fastapi import APIRouter, HTTPException
from typing import List
from src.modules.attendance.models import AttendanceEntry
from src.modules.attendance.service import AttendanceService

router = APIRouter(prefix="/attendance", tags=["attendance"])
service = AttendanceService()

@router.post("/", response_model=AttendanceEntry)
async def create_attendance(attendance: AttendanceEntry):
    return await service.create_attendance(attendance)

@router.get("/{attendance_id}", response_model=AttendanceEntry)
async def get_attendance(attendance_id: str):
    attendance = await service.get_attendance(attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance entry not found")
    return attendance

@router.get("/student/{student_id}", response_model=List[AttendanceEntry])
async def get_student_attendance(student_id: str):
    return await service.get_student_attendance(student_id)

@router.put("/{attendance_id}", response_model=AttendanceEntry)
async def update_attendance(attendance_id: str, attendance: AttendanceEntry):
    updated_attendance = await service.update_attendance(attendance_id, attendance)
    if not updated_attendance:
        raise HTTPException(status_code=404, detail="Attendance entry not found")
    return updated_attendance

@router.delete("/{attendance_id}")
async def delete_attendance(attendance_id: str):
    success = await service.delete_attendance(attendance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Attendance entry not found")
    return {"message": "Attendance entry deleted successfully"} 