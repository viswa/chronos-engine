import json
from typing import List
from pydantic import BaseModel

class TimeSettings(BaseModel):
    working_days: List[str]
    normal_days: List[str]
    special_days: List[str]

    normal_slots: List[List]
    special_slots: List[List]
    normal_breaks: List[List]
    special_breaks: List[List]

    @staticmethod
    def loadTimeSettings(fname='config/timing.json'):
        config = None
        with open(fname, 'r', encoding='utf-8') as f:
            config = json.load(f)

        needed = {
            'working_days': config['working_days'],
            'normal_days': config['normal_days'],
            'special_days': config['special_days'],
            'normal_slots': config['normal']['slots']['classes'],
            'special_slots': config['special']['slots']['classes'],
            'normal_breaks': config['normal']['slots']['breaks'],
            'special_breaks': config['special']['slots']['breaks']
        }
        return TimeSettings(**needed)
