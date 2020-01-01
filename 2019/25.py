from flask import Flask, render_template, jsonify, request
from intvm import Intcode, load, Terminal

DIRECTIONS = {
    'north': (0, -1),
    'south': (0, 1),
    'west': (-1, 0),
    'east': (1, 0),
}

program=load(day=25)

def parse(raw):
    header = None
    items = []
    navigation = None
    description = []
    head = description
    for line in raw.splitlines()[1:]:
        if not line:
            head = None
        if head is not None:
            head.append(line.lstrip(' -'))
        if line.startswith('=='):
            header = line
            head = description
        if line == 'Doors here lead:':
            navigation = []
            head = navigation
        if line == 'Items here:':
            items = []
            head = items

    return dict(
        header=header,
        description=''.join(description),
        navigation=navigation,
        items=items,
        map=game.chart())

def parse_inventory(raw):
    inv = []
    for line in raw.splitlines():
        if line.startswith('- '):
            inv.append(line[2:])
    return inv if inv else None

class State:
    def __init__(self):
        self.intcode = Intcode(program)
        self.latest = None
        self.position = (0, 0)
        self.grid = dict()

    def go(self, direction):
        if direction in DIRECTIONS:
            self.grid[self.position] = 'visited'
            dx, dy = DIRECTIONS[direction]
            x, y = self.position
            self.position = x + dx, y + dy

        data = direction
        game.intcode.write_ascii(data)
        game.intcode.write(10)
        game.latest = self.intcode.read_ascii()
        self.update_seen()
        print(self.latest)

    def update_seen(self):
        # Update seen rooms
        nav = parse(self.latest).get('navigation') or []
        x, y = self.position
        for direction in nav:
            if direction in DIRECTIONS:
                dx, dy = DIRECTIONS[direction]
                p = x + dx, y + dy
                if p not in self.grid:
                    self.grid[p] = 'seen'

    def take(self, item):
        data = "take " + request.json
        self.intcode.write_ascii(data)
        self.intcode.write(10)
        self.latest = game.intcode.read_ascii()
        print(self.latest)

    def drop(self, item):
        data = "drop " + request.json
        self.intcode.write_ascii(data)
        self.intcode.write(10)
        self.latest = game.intcode.read_ascii()
        print(self.latest)

    def chart(self):
        w, h = 16, 16
        def tojs(p, **kwargs):
            x, y = p
            d = dict(x=x + w // 2, y=y + h // 2)
            d.update(kwargs)
            return d
        rooms = []
        for p, value in self.grid.items():
            rooms.append(tojs(p, value=value))
        return dict(rooms=rooms, position=tojs(self.position))
    
    def inventory(self):
        self.intcode.write_ascii('inv\n')
        raw = self.intcode.read_ascii()
        return parse_inventory(raw)

    def json(self):
        j = parse(game.latest)
        j['inventory'] = self.inventory()
        return j

game = State()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('25.html')

@app.route('/game', methods=['GET'])
def get_game():
    if game.latest is None:
        game.latest = game.intcode.read_ascii()
        game.update_seen()
    
    return jsonify(game.json())

@app.route('/take', methods=['POST'])
def take():
    item = request.json
    game.take(item)
    return jsonify(game.json())

@app.route('/drop', methods=['POST'])
def drop():
    item = request.json
    game.drop(item)
    return jsonify(game.json())

@app.route('/go', methods=['POST'])
def go():
    direction = request.json
    game.go(direction)
    return jsonify(game.json())

if __name__ == "__main__":
    term = Terminal(Intcode(program))
    term.run()
