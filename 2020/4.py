import sys
import re

def parse_field(field):
    name, value = field.split(':', 2)
    return name, value

def parse(raw):
    fields = [parse_field(field) for field in raw.split()]
    return {name: value for name, value in fields}

def validate_height(hgt):
    if hgt.endswith('cm'):
        return 150 <= int(hgt[:-len('cm')]) <= 193
    if hgt.endswith('in'):
        return 59 <= int(hgt[:-len('in')]) <= 76
    return False

def is_valid(passport):
    #print(passport)
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    required.remove('cid')  # sneak mode
    if any(field not in passport for field in required):
        return False
    return all([
        1920 <= int(passport['byr']) <= 2002,
        2010 <= int(passport['iyr']) <= 2020,
        2020 <= int(passport['eyr']) <= 2030,
        validate_height(passport['hgt']),
        bool(re.match('^#[0-9a-f]{6}$', passport['hcl'])),
        passport['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        bool(re.match(r'^\d{9}$', passport['pid'])),
    ])

# 178 - nope
# 177 - nope

passports = [parse(raw) for raw in sys.stdin.read().split('\n\n')]
print(len([1 for passport in passports if is_valid(passport)]))
    
