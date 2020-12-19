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
    name, ranges = field.split(':')
    splat = [r.split('-', 1) for r in ranges.split('or')]
    return name, tuple(range(int(a), int(b) + 1) for a, b in splat)

def parse_ticket(raw):
    return tuple([int(i) for i in raw.split(',')])

def parse(f):
    fields, me, tickets = segments(f)
    return (
        dict(parse_field(field) for field in fields),
        parse_ticket(me[1]),
        [parse_ticket(ticket) for ticket in tickets[1:]]
    )

def matches(value, field):
    return any(value in r for r in field)

def invalid(ticket, fields):
    result = []
    for value in ticket:
        if not any(matches(value, field) for field in fields.values()):
            result.append(value)
    return result

def is_valid(ticket, fields):
    return not invalid(ticket, fields)

def field_valid(ticket_value, field):
    """Checks if field is valid at index for ticket"""
    return any(ticket_value in r for r in field)

def search(tickets, fields):
    candidates = [set(fields) for _ in fields]
    for ticket in tickets:
        for value, candidate in zip(ticket, candidates):
            for name, field in fields.items():
                if not field_valid(value, field):
                    candidate.discard(name)
    
    # find singles
    singles = {next(iter(c)) for c in candidates if len(c) == 1}
    while singles < set(fields):
        for candidate in candidates:
            if not candidate <= singles:
                candidate -= singles
        singles = {next(iter(c)) for c in candidates if len(c) == 1}
    return [next(iter(c)) for c in candidates]

fields, me, tickets = parse(sys.stdin)
tickets.append(me)
valid_tickets = [ticket for ticket in tickets if is_valid(ticket, fields)]
#print(valid_tickets)
assignment = search(valid_tickets, fields)
print(assignment)
a = 1
for name, value in zip(assignment, me):
    if name.startswith('departure'):
        a *= value
print(a)

#all_invalid = []
#for ticket in tickets:
#    all_invalid.extend(invalid(ticket, fields))
#print(sum(all_invalid))
