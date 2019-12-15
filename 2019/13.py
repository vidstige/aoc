from flask import Flask, render_template, jsonify, request

from intvm import Intcode, load
from draw import draw

vm = Intcode(program=load(day=13))
vm.program[0] = 2  # insert coin
ball = None
paddle = None

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('13.html')

@app.route('/state', methods=('DELETE',))
def reset_state():
    global vm
    vm = Intcode(program=load(day=13))
    vm.program[0] = 2  # insert coin
    vm.write(0) # dont touch joy first frame
    return jsonify('ok')

@app.route('/state', methods=('POST', 'GET'))
def state():
    # manual play
    #vm.write(request.json)
    
    score = None
    tiles = []
    while not vm.is_terminated():
        x = vm.run()
        y = vm.run()
        tile = vm.run()
        if any(v is None for v in (x, y, tile)):
            break
        if (x, y) == (-1, 0):
            score = tile
        tiles.append((x, y, tile))
    
    # autoplay
    global ball, paddle
    ball = next((x for x, y, t in tiles if t == 4), ball)
    paddle = next((x for x, y, t in tiles if t == 3), paddle)
    if paddle < ball:
        vm.write(1)
    if paddle > ball:
        vm.write(-1)

    #print(len(tiles), vm.is_terminated())
    return jsonify(dict(
        score=score,
        tiles=tiles,
        gameover=vm.is_terminated()))

if __name__ == "__main__":
    app.run()

#draw(grid)
#print(score)
#c = sys.stdin.read(1)
#print(c)
#print(len([t for t in grid.values() if t == 2]))