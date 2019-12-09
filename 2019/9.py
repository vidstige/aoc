from intvm import Intcode

def load():
    with open('input/9') as f:
        return f.read()

def parse(data):
    return [int(d) for d in data.split(',')]

ex1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
ex2 = [1102,34915192,34915192,7,4,7,99,0]
ex3 = [104,1125899906842624,99]

vm = Intcode(parse(load()))
vm.write(2)
print(vm.run_total())

