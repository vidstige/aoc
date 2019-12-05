from intvm import run, load

program = load('5')
#program = [3,0,4,0,99]
print(run(program, [5]))
#print(run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [0]))
