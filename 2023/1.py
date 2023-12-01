import sys
import re

NUMBERS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
PATTERN_FORWARD = '|'.join(['\d'] + NUMBERS)
PATTERN_BACKWARDS = '|'.join(['\d'] + [number[::-1] for number in NUMBERS])


def toint(value: str) -> str:
    try:
        return str(NUMBERS.index(value) + 1)
    except ValueError:
        return value


def calibration(line: str) -> int:
    forward = re.findall(PATTERN_FORWARD, line)
    backwards = re.findall(PATTERN_BACKWARDS, line[::-1])
    return int(toint(forward[0]) + toint(backwards[0][::-1]))


print(sum(calibration(line) for line in sys.stdin))
