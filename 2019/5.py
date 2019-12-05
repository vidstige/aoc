from intvm import run, load

program = load('5')
#program = [3,0,4,0,99]
print(run(program, [1]))

