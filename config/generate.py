from datetime import datetime
import json

TIMEFMT = '%I:%M %p'

UNASSIGNED = ('REM', 'TP')

TIMETABLE = (
    ('AAD', 'CD', 'CGIP', 'CD', 'PIP', 'REM', 'AAD'),
    ('CD', 'AAD', 'ECO', 'ECO', 'PIP', 'PIP', 'REM'),
    ('CGIP', 'NW LAB', 'NW LAB', 'NW LAB', 'TP', 'TP', 'TP'),
    ('PIP', 'CGIP', 'CD', 'CGIP', 'NW LAB', 'NW LAB', 'NW LAB'),
    ('CD', 'AAD', 'ECO', 'AAD', 'CGIP', 'COMPRE'),
)

def exportJSON(timing: dict, teacher_lookup: dict):
    """Export timetable information to json format"""

    # store for data to be exported
    exported = {
        'semester': 6,
        'department': 'cse',
        'timetable': [],
    }

    for i, wd in enumerate(timing.get('working_days')):
        wd_tt = {
            'day': wd,
            'slots': [],
        }

        day_type = None
        if wd in timing.get('normal_days'):
            day_type = timing['normal']['slots']
        else:
            day_type = timing['special']['slots']

        classes = []
        for start, end in day_type['classes']:
            start = datetime.strptime(start, TIMEFMT)
            end = datetime.strptime(end, TIMEFMT)
            classes.append((start, end))

        breaks = []
        for start, end in day_type['breaks']:
            start = datetime.strptime(start, TIMEFMT)
            end = datetime.strptime(end, TIMEFMT)
            breaks.append((start, end))

        all_hours = [*classes, *breaks]
        all_hours.sort(key=lambda x: x[0])

        classes_iterator = iter(TIMETABLE[i])

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
                subject = next(classes_iterator)
                slot_data['subject'] = subject
                slot_data['teachers'] = teacher_lookup.get(subject)

            wd_tt['slots'].append(slot_data)
        exported['timetable'].append(wd_tt)
    
    with open('generated.json', 'w') as f:
        f.write(json.dumps(exported, indent=2))

def main():
    mapping = None
    with open('mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)['course_mapping']

    lookup = {course['internal_code']: course['teacher_codes'] for course in mapping}
    
    timing = None
    with open('timing.json', 'r', encoding='utf-8') as f:
        timing = json.load(f)
    
    if not len(timing['working_days']) == len(TIMETABLE):
        print('Oops!')

    exportJSON(timing, lookup)
    # print(lookup)

if __name__ == '__main__':
    main()
