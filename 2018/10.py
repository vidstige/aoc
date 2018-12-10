import re

from flask import Flask, render_template, jsonify

app = Flask(__name__)

def load():
    pattern = r'position=<\s*([-\d]+),\s*([-\d]+)> velocity=<\s*([-\d]+),\s*([-\d]+)>'
    with open('input/10') as f:
        for line in f:
            match = re.match(pattern, line)
            if match:
                x, y, dx, dy = match.groups()
                yield (int(x), int(y)), (int(dx), int(dy))


def add(a, b, step):
    x, y = a
    dx, dy = b
    return x + dx * step, -(y + dy * step)

def normalize(p):
    xmin, xmax = min(x for x, _ in p), max(x for x, _ in p)
    ymin, ymax = min(y for _, y in p), max(y for _, y in p)
    w = xmax - xmin
    h = ymax - ymin
    return [((x - xmin)/w, (y - ymin)/h) for x, y in p]

def area(p):
    xmin, xmax = min(x for x, _ in p), max(x for x, _ in p)
    ymin, ymax = min(y for _, y in p), max(y for _, y in p)
    w = xmax - xmin
    h = ymax - ymin
    return w * h

points = list(load())
deltas = [d for _, d in points]

@app.route('/')
def index():
    return render_template('10.html')

@app.route('/cords/<int:step>')
def coordinates(step: int):
    p = [add(p, dp, step) for p, dp in points]
    return jsonify(normalize(p))

import matplotlib.pyplot as plt
p = [add(p, dp, 10159) for p, dp in points]
plt.scatter(*zip(*p))
plt.show()
