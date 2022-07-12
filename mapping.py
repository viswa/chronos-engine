import json
from typing import List, Optional

from pydantic import BaseModel

class CourseTeacherMapping(BaseModel):
    course_no: str
    internal_code: str
    venue: Optional[str]
    teacher_codes: List[str]
    shared: Optional[bool]
    other: Optional[str]

    @staticmethod
    def loadMapping(fname='config/mapping.json'):
        mapping = None
        with open(fname, 'r', encoding='utf-8',) as f:
            mapping = json.load(f)
        
        mappings = []
        for mp in mapping['course_mapping']:
            mappings.append(CourseTeacherMapping(**mp))
        return mappings
