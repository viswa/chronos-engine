import json

from pydantic import BaseModel

class Course(BaseModel):
    course_no: str
    course_name: str
    credit: int

    @staticmethod
    def loadCourses(fname='config/courses.json'):
        obj = None # course object
        with open(fname, 'r', encoding='utf-8') as f:
            obj = json.load(f)

        courses = []
        for crs in obj['courses']:
            course = Course(**crs)
            courses.append(course)
        return courses
