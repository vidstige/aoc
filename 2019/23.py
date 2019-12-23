from intvm import Intcode, load

def main():
    program = load(day=23)
    machines = [Intcode(program) for _ in range(50)]
    queues = [[] for _ in range(50)]
    polling = [False] * 50

    nat = None

    for i, machine in enumerate(machines):
        machine.write(i)

    while True:
        for i, (machine, queue) in enumerate(zip(machines, queues)):
            if queue:
                ix, iy = queue.pop(0)
                machine.write(ix)
                machine.write(iy)
            else:
                machine.write(-1)

            a = machine.run()
            polling[i] = a is None
            if a is not None:
                x = machine.run()
                y = machine.run()
                if a == 255:
                    #print("sending {}, {} to NAT")
                    nat = (x, y)
                else:
                    #print("sending {}, {} to {}".format(x, y, a))
                    queues[a].append((x, y))
            
            if all(polling) and all(not q for q in queues):
                x, y = nat
                print(x, y)
                queues[0].append((x, y))
                

main()
