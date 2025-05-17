def get_attendance_sms_template(guardian_name: str, student_name: str, student_section: str, date_str: str, time_str: str, is_time_in: bool) -> str:
    status = "arrived in" if is_time_in else "departed from"
    section_info = f" of {student_section}" if student_section else ""
    
    return f"""[JCFA System]
Attendance Monitoring Notification

Hi {guardian_name}, this is to inform you that {student_name}{section_info} has {status} JFCA school premises at {date_str} {time_str}

Thank you""" 