import re
from typing import Tuple
from collections import defaultdict
import operator


class Event(object):
    def __init__(self, event):
        self.event = event
    
    def guard(self):
        match = re.search(r'#(\d+)', self.event)
        if match:
            return int(match.group(1))
        return None
    
    def falls_asleep(self) -> bool:
        return self.event == 'falls asleep'
    
    def wakes_up(self) -> bool:
        return self.event == 'wakes up'

    def __str__(self):
        return self.event


def load():
    with open('input/4') as f:
        for i, line in enumerate(f):
            pattern = r'\[(\d\d\d\d-\d\d-\d\d) (\d\d):(\d\d)\] (.*)'
            match = re.match(pattern, line)
            if match:
                date, hours, minutes, event = match.groups()
                yield date, int(hours), int(minutes), i, Event(event)
    
guard = None
asleep_since = ('', 0)
total_sleep = defaultdict(int)
minute_split = defaultdict(lambda: [0] * 60)
for date, hours, minutes, _, event in sorted(load()):
    print(date, hours, minutes, event)
    if event.guard():
        guard = event.guard()
        
        asleep_since = None
    else:
        if asleep_since:
            date_start, hours_start, minutes_start = asleep_since
            total_sleep[guard] += minutes - minutes_start
            for m in range(minutes_start, minutes):
                if date != date_start:
                    print('warn: different dates')
                minute_split[guard][m] += 1
            asleep_since = None
        else:
            asleep_since = date, hours, minutes

most_sleeping_guard = max(total_sleep, key=total_sleep.get)
index, value = max(enumerate(minute_split[most_sleeping_guard]), key=operator.itemgetter(1))    
print(most_sleeping_guard, index)
print(most_sleeping_guard * index)
