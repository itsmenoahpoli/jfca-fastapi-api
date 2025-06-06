from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException
import pytz

from src.database.entities import AttendanceEntity, StudentEntity, SectionEntity
from src.modules.attendance.attendance_dto import AttendanceCreateDTO, AttendanceUpdateDTO, TimeInOutDTO
from src.modules.notifications.notifications_service import notifications_service
from src.modules.attendance.sms_templates import get_attendance_sms_template


class AttendanceService:
    def __init__(self):
        self.entity = AttendanceEntity

    def create_attendance(self, data: AttendanceCreateDTO) -> dict:
        attendance_data = {
            'student_id': data.student_id,
            'status': data.status,
            'notes': data.notes,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = self.entity.insert_one(attendance_data)
        attendance_data['_id'] = str(result.inserted_id)
        return attendance_data

    def get_attendance(self, attendance_id: str) -> Optional[dict]:
        result = self.entity.find_one({'_id': ObjectId(attendance_id)})
        if result:
            result['_id'] = str(result['_id'])
        return result

    def get_student_attendance(self, student_id: str) -> List[dict]:
        results = list(self.entity.find({'student_id': student_id}))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def get_attendance_by_date(self, date: datetime) -> List[dict]:
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = datetime(date.year, date.month, date.day, 23, 59, 59)
        results = list(self.entity.find({
            'created_at': {
                '$gte': start_of_day,
                '$lte': end_of_day
            }
        }))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def update_attendance(self, attendance_id: str, data: AttendanceUpdateDTO) -> Optional[dict]:
        update_data = {}
        if data.status is not None:
            update_data['status'] = data.status
        if data.notes is not None:
            update_data['notes'] = data.notes
        update_data['updated_at'] = datetime.now()
        
        result = self.entity.update_one(
            {'_id': ObjectId(attendance_id)},
            {'$set': update_data}
        )
        if result.modified_count > 0:
            return self.get_attendance(attendance_id)
        return None

    def delete_attendance(self, attendance_id: str) -> bool:
        result = self.entity.delete_one({'_id': ObjectId(attendance_id)})
        return result.deleted_count > 0

    def get_all_attendance(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
        try:
            query = {}
            
            if start_date or end_date:
                date_filter = {}
                if start_date:
                    date_filter['$gte'] = start_date
                if end_date:
                    end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)
                    date_filter['$lte'] = end_date
                query['date_recorded'] = date_filter
            
            results = list(self.entity.find(query).sort('created_at', -1))
            formatted_results = []
            
            for result in results:
                try:
                    attendance_data = {
                        '_id': str(result['_id']),
                        'student_id': result.get('student_id'),
                        'date_recorded': result.get('date_recorded'),
                        'time_in': result.get('time_in'),
                        'time_out': result.get('time_out'),
                        'in_status': result.get('in_status', False),
                        'out_status': result.get('out_status', False),
                        'sms_notif_status': result.get('sms_notif_status', 'pending'),
                        'created_at': result.get('created_at'),
                        'updated_at': result.get('updated_at')
                    }
                    
                    if result.get('student_id'):
                        try:
                            student = StudentEntity.find_one({'_id': ObjectId(result['student_id'])})
                            if student:
                                student_data = {
                                    '_id': str(student['_id']),
                                    'name': f"{student.get('first_name', '')} {student.get('middle_name', '')} {student.get('last_name', '')}".strip(),
                                    'first_name': student.get('first_name', ''),
                                    'middle_name': student.get('middle_name', ''),
                                    'last_name': student.get('last_name', ''),
                                    'guardian_name': student.get('guardian_name'),
                                    'guardian_mobile': student.get('guardian_mobile'),
                                    'section_id': str(student.get('section_id', ''))
                                }
                                
                                if student.get('section_id'):
                                    try:
                                        section = SectionEntity.find_one({'_id': ObjectId(student['section_id'])})
                                        if section:
                                            section_data = {
                                                '_id': str(section['_id']),
                                                'name': section.get('name', ''),
                                                'grade_level': section.get('grade_level')
                                            }
                                            student_data['section'] = section_data
                                    except Exception:
                                        pass
                                
                                attendance_data['student'] = student_data
                        except Exception:
                            pass
                    
                    formatted_results.append(attendance_data)
                except Exception:
                    continue
            
            return formatted_results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving attendance records: {str(e)}")

    def record_time_in_out(self, data: TimeInOutDTO) -> dict:
        try:
            student = StudentEntity.find_one({'_id': ObjectId(data.student_id)})
            if not student:
                raise HTTPException(status_code=404, detail='Student not found')

            now = datetime.now()
            start_of_day = datetime(now.year, now.month, now.day)
            end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

            print('Query parameters:')
            print('student_id:', data.student_id)
            print('start_of_day:', start_of_day)
            print('end_of_day:', end_of_day)

            query = {
                'student_id': data.student_id,
                'date_recorded': {
                    '$gte': start_of_day,
                    '$lte': end_of_day
                }
            }
            print('MongoDB query:', query)

            existing_record = self.entity.find_one(query)
            print('existing_record:', existing_record)

            if existing_record:
                if existing_record.get('out_status'):
                    raise HTTPException(status_code=400, detail='Student has already completed attendance for today')
                
                update_data = {
                    'time_out': now,
                    'out_status': True,
                    'updated_at': now
                }
                self.entity.update_one(
                    {'_id': existing_record['_id']},
                    {'$set': update_data}
                )

                student_name = student.get('name', 'Student')
                section = SectionEntity.find_one({'_id': ObjectId(student.get('section_id'))})
                student_section = section.get('name', 'Unknown Section') if section else 'Unknown Section'
                guardian_name = student.get('guardian_name', 'Guardian')
                guardian_mobile = student.get('guardian_mobile_number', '')
                time_str = now.strftime('%I:%M %p')
                date_str = now.strftime('%B %d, %Y')
                message = get_attendance_sms_template(guardian_name, student_name, student_section, date_str, time_str, False)

                sms_sent = notifications_service.send_sms(guardian_mobile, message)
                
                self.entity.update_one(
                    {'_id': existing_record['_id']},
                    {'$set': {'sms_notif_status': 'sent' if sms_sent else 'failed'}}
                )

                updated_record = self.entity.find_one({'_id': existing_record['_id']})
                updated_record['_id'] = str(updated_record['_id'])

                return {
                    'id': str(updated_record['_id']),
                    'student_id': data.student_id,
                    'date_recorded': updated_record['date_recorded'].strftime('%Y-%m-%d'),
                    'time_in': updated_record['time_in'].strftime('%H:%M:%S') if updated_record['time_in'] else None,
                    'time_out': updated_record['time_out'].strftime('%H:%M:%S') if updated_record['time_out'] else None,
                    'in_status': updated_record['in_status'],
                    'out_status': updated_record['out_status'],
                    'sms_notif_status': 'sent' if sms_sent else 'failed',
                    'message': 'Time out recorded successfully'
                }
            else:
                attendance_data = {
                    'student_id': data.student_id,
                    'date_recorded': now,
                    'time_in': now,
                    'time_out': None,
                    'in_status': True,
                    'out_status': False,
                    'sms_notif_status': 'pending',
                    'created_at': now,
                    'updated_at': now
                }
                result = self.entity.insert_one(attendance_data)
                record_id = result.inserted_id

                student_name = student.get('name', 'Student')
                section = SectionEntity.find_one({'_id': ObjectId(student.get('section_id'))})
                student_section = section.get('name', 'Unknown Section') if section else 'Unknown Section'
                guardian_name = student.get('guardian_name', 'Guardian')
                guardian_mobile = student.get('guardian_mobile_number', '')
                time_str = now.strftime('%I:%M %p')
                date_str = now.strftime('%B %d, %Y')
                message = get_attendance_sms_template(guardian_name, student_name, student_section, date_str, time_str, True)
                
                sms_sent = notifications_service.send_sms(guardian_mobile, message)
                
                self.entity.update_one(
                    {'_id': record_id},
                    {'$set': {'sms_notif_status': 'sent' if sms_sent else 'failed'}}
                )

                updated_record = self.entity.find_one({'_id': record_id})
                updated_record['_id'] = str(updated_record['_id'])

                return {
                    'id': str(record_id),
                    'student_id': data.student_id,
                    'date_recorded': updated_record['date_recorded'].strftime('%Y-%m-%d'),
                    'time_in': updated_record['time_in'].strftime('%H:%M:%S') if updated_record['time_in'] else None,
                    'time_out': updated_record['time_out'].strftime('%H:%M:%S') if updated_record['time_out'] else None,
                    'in_status': updated_record['in_status'],
                    'out_status': updated_record['out_status'],
                    'sms_notif_status': 'sent' if sms_sent else 'failed',
                    'message': 'Time in recorded successfully'
                }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) 