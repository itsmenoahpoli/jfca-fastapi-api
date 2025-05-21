import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.modules.students.students_service import students_service

def main():
    print("Starting mobile number formatting update...")
    result = students_service.format_all_student_mobile_numbers()
    print(result["message"])

if __name__ == "__main__":
    main() 