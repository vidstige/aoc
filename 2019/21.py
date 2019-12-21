from intvm import Intcode, load


# ABC
##.#.##

# A! AND B AND !C

#@ABCDEFGHI
####.#.##.#.####

#   J
#####...#########

#  J
#####..#.########

vm = Intcode(program=load(day=21))

# ABCDEFGHI
#@   @   @

# Jump if any space (unless !A AND B AND !C) and double landing spaces ok
# !(A AND AND B C OR) AND D AND (H OR E)

#ABCDEFGHI
#.#.##.#.####

program = """
NOT T T
AND A T
AND B T
AND C T
NOT T J
AND D J
NOT A T
AND A T
OR H T
OR E T
AND T J
RUN
"""

vm.write_ascii(program.lstrip())
while not vm.is_terminated():
    c = vm.run()
    if c is not None:
        if c > 255:
            print(c)
            break
        print(str(chr(c)), end='')
