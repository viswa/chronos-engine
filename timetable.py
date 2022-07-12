from datetime import datetime

import random
import json

class TimeTable:
    """TimeTable class represents a timetable represented a heteregenous
    matrix.
    Each row of the `days` list represents the schedule for a day.
    """

    def __init__(self, settings):
        self.days = []
        for wd in settings.working_days:
            if wd in settings.normal_days:
                self.days.append([None] * len(settings.normal_slots))
            else:
                self.days.append([None] * len(settings.special_slots))

    def generate(self, courses):
        """Generate a timetable based on simple constraints"""
        course_count = dict.fromkeys(map(lambda c: c.course_no, courses), 0)

        # All core subjects get a first hour
        core = list(filter(lambda c: c.credit > 2 and  c.course_no.startswith("CS"), courses))
        random.shuffle(core)
        core.append(random.choice(core)) # Duplicate a course for testing
        for i, day in enumerate(self.days):
            day[0] = core[i]
            course_count[day[0].course_no] += 1

        # Labs together
        lab = next(filter(lambda c: c.course_no.split()[0].endswith('L'), courses))
        lab_days = random.sample(range(5), k=2)
        for day in lab_days:
            start = 0
            if len(self.days[day]) == 7:
                start = random.choice([1, 4])
            else:
                start = 1
            for i in range(3):
                self.days[day][start + i] = lab
        course_count[lab.course_no] += 3

        # Core subjects get credit + 1 hours weekly
        core.pop() # Remove a duplicate from core
        for course in core:
            # Assign each core course first
            while course_count[course.course_no] < course.credit + 1:
                day = 0
                while True:
                    day = random.choice(range(5))
                    count = 0
                    for crs in self.days[day]:
                        if crs is None:
                            continue
                        if crs.course_no == course.course_no:
                            count += 1
                    if count > 1:
                        continue
                    break

                available = [i for i, c in enumerate(self.days[day]) if c is None]
                if not available:
                    continue
                random.shuffle(available)
                hour = random.choice(available)

                self.days[day][hour] = course
                course_count[course.course_no] += 1

        # Assign other subjects
        other = list(filter(lambda c: c.credit < 2 or not c.course_no.startswith("CS"), courses))
        for course in other:
            while course_count[course.course_no] < course.credit:
                day = 0
                while True:
                    day = random.choice(range(5))
                    count = 0
                    for crs in self.days[day]:
                        if crs is None:
                            continue
                        if crs.course_no == course.course_no:
                            count += 1
                    if count > 1:
                        continue
                    break

                available = [i for i, c in enumerate(self.days[day]) if c is None]
                if not available:
                    continue
                random.shuffle(available)
                hour = random.choice(available)

                self.days[day][hour] = course
                course_count[course.course_no] += 1

    def exportJSON(self, time_settings, courses, mappings, filename='export.json'):
        """Export timetable information to json format"""
        TIMEFMT = '%I:%M %p'

        course_lookup = dict.fromkeys(map(lambda c: c.course_no, courses))
        for mapping in mappings:
            course_lookup[mapping.course_no] = mapping

        # store for data to be exported
        exported = {
            'semester': 6,
            'department': 'cse',
            'timetable': [],
        }

        for i, wd in enumerate(time_settings.working_days):
            wd_tt = {
                'day': wd,
                'slots': [],
            }

            class_type = None
            if wd in time_settings.normal_days:
                class_type = time_settings.normal_slots
                break_type = time_settings.normal_breaks
            else:
                class_type = time_settings.special_slots
                break_type = time_settings.special_breaks

            classes = []
            for start, end in class_type:
                start = datetime.strptime(start, TIMEFMT)
                end = datetime.strptime(end, TIMEFMT)
                classes.append((start, end))

            breaks = []
            for start, end in break_type:
                start = datetime.strptime(start, TIMEFMT)
                end = datetime.strptime(end, TIMEFMT)
                breaks.append((start, end))

            all_hours = [*classes, *breaks]
            all_hours.sort(key=lambda x: x[0])

            classes_iterator = iter(self.days[i])
            for hour in all_hours:
                slot_data = {
                    'time': [
                        datetime.strftime(hour[0], TIMEFMT),
                        datetime.strftime(hour[1], TIMEFMT),
                    ],
                    'break': False,
                }

                if hour in breaks:
                    slot_data['break'] = True
                else:
                    course = next(classes_iterator)
                    if course is None:
                        slot_data['course'] = 'VAC'
                        slot_data['teachers'] = ''
                    else:
                        if course_lookup[course.course_no].shared:
                            slot_data['course'] = [
                                course_lookup[course.course_no].internal_code,
                                course_lookup[course_lookup[course.course_no].other].internal_code,
                            ]
                            teachers = set(course_lookup[course.course_no].teacher_codes)
                            teachers.union(course_lookup[course_lookup[course.course_no].other].teacher_codes)
                            slot_data['teachers'] = list(teachers)
                        else:
                            slot_data['course'] = course_lookup[course.course_no].internal_code
                            slot_data['teachers'] = course_lookup[course.course_no].teacher_codes
                wd_tt['slots'].append(slot_data)
            exported['timetable'].append(wd_tt)
    
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(exported, indent=2))

    def printTT(self, courses, course_mapping):
        course_lookup = dict.fromkeys(map(lambda c: c.course_no, courses))
        for mapping in course_mapping:
            course_lookup[mapping.course_no] = mapping.internal_code
        # print(course_lookup)
        for day in self.days:
            for slot in day:
                if slot:
                    print(f'{course_lookup[slot.course_no]:<10}', end=' | ')
                else:
                    print(f'{"Empty":<10}', end=' | ')
            print()
