from itertools import permutations, cycle
from pathlib import Path
from intvm import Intcode

def load():
    no = Path(__file__).stem
    with open('input/{}'.format(no)) as f:
        return f.read()
def parse(data):
    return [int(d) for d in data.split(',')]

def amplifier(program, settings):
    i = 0
    for setting in settings:
        amp = Intcode(program.copy())
        outputs = amp.run(data=[i, setting])
        i = outputs
    return outputs

def amplifier_feedback(program, settings):
    amps = [Intcode(program.copy()) for _ in settings]
    for amp, setting in zip(amps, settings):
        amp.write(setting)

    last_e = None
    amps[0].write(0)
    i = 0
    for index, amp in cycle(enumerate(amps)):
        #print(i, index, len([a for a in amps if not a.is_terminated()]))
        output = amp.run()
        if output is not None:
            amps[(index+1) % len(amps)].write(output)
            if index == len(settings) - 1:
                last_e = output
        if all(a.is_terminated() for a in amps):
            break
        i += 1
    #print(last_e)
    return last_e

def optimize(program):
    settings = permutations(range(5, 10))
    return max((amplifier_feedback(program, setting), setting) for setting in settings)

ex1=[3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
ex2=[3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
ex3=[3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]

ex4=[3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
ex5=[3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

#print(optimize(ex1))
#print(optimize(ex2))
#print(optimize(ex3))
#print(optimize(ex4))
#print(optimize(ex5))
print(optimize(parse(load())))

# bad: 9124423
