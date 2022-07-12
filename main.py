import json

from fastapi import FastAPI

from timetable import TimeTable

import course
import mapping
import timing

app = FastAPI()
timetables = []

@app.get('/')
def index():
    """Make sure things are working"""
    return {'message': 'working'}

@app.get('/exists')
def check_timetable():
    """Check whether exisitng timetables are found"""
    if not timetables:
        return {'message': 'no timetables'}
    return {'message': f'{len(timetables)} available'}

@app.get('/create')
def create_timetable():
    """Create a timetable. Do not sent data to the API. All configurations are internal"""
    print('Creating timetable')
    time_settings = timing.TimeSettings.loadTimeSettings()
    courses = sorted(course.Course.loadCourses(), key=lambda c: c.credit, reverse=True)
    course_mapping = mapping.CourseTeacherMapping.loadMapping()
    tt = TimeTable(time_settings)
    tt.generate(courses)
    print('Creation phase complete')
    tt.printTT(courses, course_mapping)

    print('Exporting to JSON')
    filename = f'export{len(timetables)}.json'
    tt.exportJSON(time_settings, courses, course_mapping, filename)
    timetables.append(filename)
    print(f'JSON available for fetching at index `{len(timetables) - 1}`')
    return {'message': f'{len(timetables)} available'}

@app.get('/timetable/{id}')
def send_timetable(id: int):
    """Return a timetable available at index `id`"""
    filename = None
    try:
        filename = timetables[id]
    except IndexError:
        return {'error': 'invalid index'}
    
    contents = None
    with open(filename, 'r', encoding='utf-8') as f:
        contents = json.load(f)
    return contents
