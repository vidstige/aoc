from itertools import permutations
from pathlib import Path
from intvm import run

def load():
    no = Path(__file__).stem
    with open('input/{}'.format(no)) as f:
        return f.read()
def parse(data):
    return [int(d) for d in data.split(',')]

def amplifier(program, settings):
    i = 0
    for setting in settings:
        amp = program.copy()
        outputs = run(amp, data=[i, setting])
        i = outputs[0]
    return outputs[0]

def optimize(program):
    settings = permutations(range(5))
    return max(amplifier(program, setting) for setting in settings)

ex1=[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
ex2=[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
ex3=[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

print(optimize(ex1))
print(optimize(ex2))
print(optimize(ex3))
print(optimize(parse(load())))