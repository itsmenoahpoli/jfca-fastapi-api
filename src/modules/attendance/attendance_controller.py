from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from src.modules.attendance.attendance_dto import (
    AttendanceCreateDTO, AttendanceResponseDTO, AttendanceUpdateDTO, TimeInOutDTO,
    TimeInOutResponseDTO
)
from src.modules.attendance.attendance_service import AttendanceService

attendance_router = APIRouter(prefix='/attendance', tags=['Attendance'])
service = AttendanceService()


@attendance_router.post('', response_model=AttendanceResponseDTO)
def create_attendance(attendance: AttendanceCreateDTO):
    try:
        return service.create_attendance(attendance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@attendance_router.get('/{attendance_id}', response_model=AttendanceResponseDTO)
def get_attendance(attendance_id: str):
    attendance = service.get_attendance(attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail='Attendance record not found')
    return attendance


@attendance_router.get('/student/{student_id}', response_model=List[AttendanceResponseDTO])
def get_student_attendance(student_id: str):
    return service.get_student_attendance(student_id)


@attendance_router.get('/date/{date}', response_model=List[AttendanceResponseDTO])
def get_attendance_by_date(date: str):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        return service.get_attendance_by_date(date_obj)
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid date format. Use YYYY-MM-DD')


@attendance_router.get('', response_model=List[TimeInOutResponseDTO])
def get_all_attendance():
    try:
        return service.get_all_attendance()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@attendance_router.patch('/{attendance_id}', response_model=AttendanceResponseDTO)
def update_attendance(attendance_id: str, attendance: AttendanceUpdateDTO):
    updated = service.update_attendance(attendance_id, attendance)
    if not updated:
        raise HTTPException(status_code=404, detail='Attendance record not found')
    return updated


@attendance_router.delete('/{attendance_id}')
def delete_attendance(attendance_id: str):
    deleted = service.delete_attendance(attendance_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Attendance record not found')
    return {'message': 'Attendance record deleted successfully'}


@attendance_router.post('/time-in-out')
def record_time_in_out(data: TimeInOutDTO):
    try:
        result = service.record_time_in_out(data)
        return result
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail='Student not found')
        elif e.status_code == 400:
            raise HTTPException(status_code=400, detail='Student has already completed attendance for today')
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 