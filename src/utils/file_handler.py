import json
from typing import List
from ..models.studente import Studente

class FileHandler:
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def load_students(self) -> List[Studente]:
        try:
            with open(self.file_path, encoding=self.encoding) as file:
                data = json.load(file)
                return [Studente.from_dict(student_data) for student_data in data]
        except (json.JSONDecodeError, FileNotFoundError):
            print("❌ Error in JSON file or file not found.")
            return []

    def save_students(self, students: List[Studente]) -> bool:
        try:
            data = [student.to_dict() for student in students]
            with open(self.file_path, 'w', encoding=self.encoding) as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False