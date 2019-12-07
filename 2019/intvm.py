def load(day):
    with open('input/{day}'.format(day=day)) as f:
        return [int(x) for x in f.read().split(',')]

class Intcode:
    def __init__(self, program):
        self.program = program
        self.ip = 0
        self.data = []

    def write(self, data):
        self.data.append(data)

    def _parameter(self, i, modes):
        value = self.program[self.ip + i]
        if modes[i] == 0:
            return self.program[value]
        return value

    def run(self):
        while True:
            opcode = self.program[self.ip] % 100
            pm = self.program[self.ip] // 100
            self.ip += 1
            modes = []
            for _ in range(3):
                modes.append(pm % 10)
                pm = pm // 10

            if opcode == 1:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                destination = self.program[self.ip + 2]
                self.program[destination] = a + b
                self.ip += 3
            elif opcode == 2:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                destination = self.program[self.ip + 2]
                self.program[destination] = a * b
                self.ip += 3
            elif opcode == 3:
                destination = self.program[self.ip]
                self.program[destination] = self.data.pop(0)
                self.ip += 1
            elif opcode == 4:
                #ource = self.program[self.ip]
                #return self.program[source]
                #out.append(self.program[source])
                tmp = self._parameter(0, modes)
                self.ip += 1
                return tmp
            elif opcode == 5:
                condition = self._parameter(0, modes)
                jump = self._parameter(1, modes)
                if condition:
                    self.ip = jump
                else:
                    self.ip += 2
            elif opcode == 6:
                condition = self._parameter(0, modes)
                jump = self._parameter(1, modes)
                if not condition:
                    self.ip = jump
                else:
                    self.ip += 2
            elif opcode == 7:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                destination = self.program[self.ip + 2]
                self.program[destination] = 1 if a < b else 0
                self.ip += 3
            elif opcode == 8:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                destination = self.program[self.ip + 2]
                self.program[destination] = 1 if a == b else 0
                self.ip += 3
            elif opcode == 99:
                break
            else:
                raise ValueError('bad opcode: {}'.format(opcode))
        # terminated
        self.ip -= 1
        return None

    def is_terminated(self):
        return self.program[self.ip] % 100 == 99
