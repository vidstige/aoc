def load(day):
    with open('input/{day}'.format(day=day)) as f:
        return [int(x) for x in f.read().split(',')]

class Intcode:
    def __init__(self, program):
        self.program = program
        self.ip = 0
        self.data = []
        self.relative_base = 0

    def write(self, data):
        self.data.append(data)

    def _grow(self, address: int) -> int:
        """Grows memory if needed"""
        self.program.extend([0] * (address - len(self.program) + 1))

    def _get(self, address: int):
        self._grow(address)
        return self.program[address]

    def _write(self, i, modes, values):
        address = self._get(self.ip + i)
        mode = modes[i]
        if mode == 0:
            self._grow(address)
            self.program[address] = values
        elif mode == 2:
            self._grow(self.relative_base + address)
            self.program[self.relative_base + address] = values
        else:
            raise Exception('Unknown mode: {mode}'.format(mode=mode))

    def _parameter(self, i, modes):
        value = self._get(self.ip + i)
        mode = modes[i]
        if mode == 0:
            return self._get(value)
        if mode == 1:
            return value
        if mode == 2:
            return self._get(self.relative_base + value)
        raise Exception('Unknown mode: {mode}'.format(mode=mode))

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
                self._write(2, modes, a + b)
                self.ip += 3
            elif opcode == 2:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                self._write(2, modes, a * b)
                self.ip += 3
            elif opcode == 3:
                #destination = self._get(self.ip)
                value = self.data.pop(0)
                self._write(0, modes, value)
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
                self._write(2, modes, 1 if a < b else 0)
                self.ip += 3
            elif opcode == 8:
                a = self._parameter(0, modes)
                b = self._parameter(1, modes)
                self._write(2, modes, 1 if a == b else 0)
                self.ip += 3
            elif opcode == 9:
                self.relative_base += self._parameter(0, modes)
                self.ip += 1
            elif opcode == 99:
                break
            else:
                raise ValueError('bad opcode: {}'.format(opcode))
        # terminated
        self.ip -= 1
        return None
    
    def run_total(self):
        out = []
        while True:
            o = self.run()
            if o is None:
                return out
            out.append(o)

    def is_terminated(self):
        return self.program[self.ip] % 100 == 99
