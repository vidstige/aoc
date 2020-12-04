import sys

def parse_field(field):
    name, value = field.split(':', 2)
    return name, value

def parse(raw):
    fields = [parse_field(field) for field in raw.split()]
    return {name: value for name, value in fields}

def is_valid(passport, required):
    return all(field in passport for field in required)

passports = sys.stdin.read().split('\n\n')
required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
required.remove('cid')  # sneak mode
print(len([1 for passport in passports if is_valid(passport, required)]))
    
