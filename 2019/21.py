from intvm import Intcode, load
    
#   J
#####...#########

#  J
#####..#.########

vm = Intcode(program=load(day=21))

# A AND !(!C AND D)
program = """
NOT C T
AND D T
NOT T T
AND A T
NOT T J
WALK
"""

vm.write_ascii(program.lstrip())
while not vm.is_terminated():
    c = vm.run()
    if c is not None:
        if c > 255:
            print(c)
            break
        print(str(chr(c)), end='')
