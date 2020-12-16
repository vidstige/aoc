import sys

def segments(f):
    parts = [[]]
    for line_n in f:
        line = line_n.strip()
        if line:
            parts[-1].append(line)
        else:
            parts.append([])
    return parts

def parse_field(field):
    _name, ranges = field.split(':')
    splat = [r.split('-', 1) for r in ranges.split('or')]
    return [range(int(a), int(b) + 1) for a, b in splat]

def parse_ticket(raw):
    return tuple([int(i) for i in raw.split(',')])

def parse(f):
    fields, my, tickets = segments(f)
    return (
        [parse_field(field) for field in fields],
        None,
        [parse_ticket(ticket) for ticket in tickets[1:]]
    )

def matches(value, field):
    return any(value in r for r in field)

def invalid(ticket, fields):
    for value in ticket:
        if not any(matches(value, field) for field in fields):
            yield value
    return []

fields, _me, tickets = parse(sys.stdin)
all_invalid = []
for ticket in tickets:
    all_invalid.extend(invalid(ticket, fields))
print(sum(all_invalid))
