import re
import sys
from typing import Dict, List, Optional, TextIO

class Rule:
    def __init__(self, target: str) -> None:
        self.target = target

    def apply(self, part: Dict[str, int]) -> Optional[str]:
        del part
        return None

class Less(Rule):
    PATTERN = '([a-z]+)<(\d+):([a-z]+|A|R)'
    def __init__(self, target: str, property: str, value: int) -> None:
        super().__init__(target)
        self.property = property
        self.value = value

    def apply(self, part: Dict[str, int]) -> Optional[str]:
        if part[self.property] < self.value:
            return self.target
        return None


class More(Rule):
    PATTERN = '([a-z]+)>(\d+):([a-z]+|A|R)'
    def __init__(self, target: str, property: str, value: int) -> None:
        super().__init__(target)
        self.property = property
        self.value = value

    def apply(self, part: Dict[str, int]) -> Optional[str]:
        if part[self.property] > self.value:
            return self.target
        return None

class Unconditional(Rule):
    def __init__(self, target: str) -> None:
        super().__init__(target)        

    def apply(self, part: Dict[str, int]) -> Optional[str]:
        return self.target


def parse_rule(r: str) -> Rule:
    match = re.match(Less.PATTERN, r)
    if match:
        property, value, target = match.groups()
        return Less(target, property, int(value))
    match = re.match(More.PATTERN, r)
    if match:
        property, value, target = match.groups()
        return More(target, property, int(value))
    return Unconditional(r)


def accept(rules: Dict[str, List[Rule]], part: Dict[str, int], start: str = 'in') -> bool:
    workflow = start
    while workflow not in ('R', 'A'):
        workflow = next(r.apply(part) for r in rules[workflow] if r.apply(part) is not None)
    return workflow == 'A'
    
def parse(f: TextIO):
    PATTERN = r'([a-z]+){(.*)}'
    lines = (line.rstrip() for line in f)
    rules = {}
    for line in lines:
        if not line:
            break
        match = re.match(PATTERN, line)
        if match:
            name, rest = match.groups()
            rules[name] = [parse_rule(r) for r in rest.split(',')]

    total = 0
    for line in lines:
        part = {}
        for property in line.lstrip('{').rstrip('}').split(','):
            name, value = property.split('=')
            part[name] = int(value)
        if accept(rules, part):
            total += sum(part.values())
    print(total)
        

parse(sys.stdin)
