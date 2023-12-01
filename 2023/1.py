import sys
import re


def calibration(line: str) -> int:
    numbers = re.findall('\d', line)
    return int(numbers[0] + numbers[-1])

lines = [line.rstrip() for line in sys.stdin]
print(sum(calibration(line) for line in lines))    
