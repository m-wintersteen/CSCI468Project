
class Translator:

    def __init__(self):
        self.r = -1


    def getRegister(self):
        self.r = self.r + 1
        return 'r{}'.format(self.r)


    def translate(self, code, symbolTable):
        assembly = []
        regmap = {}
        for id in symbolTable:
            assembly.append('var {}'.format(id))
        for line in code:
            [instr, *args] = line.split(' ')
            if len(args) == 3:
                pass
                # op1 = Executor.registers[args[0]]
                # op2 = Executor.registers[args[1]]
                # result = None
                # if (instr == 'ADDI'):
                #     result = op1 + op2
                # elif (instr == 'SUBI'):
                #     result = op1 - op2
                # elif (instr == 'MULTI'):
                #     result = op1 * op2
                # elif (instr == 'DIVI'):
                #     result = op1 / op2
                # Executor.registers[args[2]] = result
            elif len(args) == 2:
                if args[1][0] == '$':
                    regmap[args[1]] = self.getRegister
                    assembly.append('move {} {}'.format(args[0], regmap[args[1]]))
                else:
                    assembly.append('move {} {}'.format(regmap[args[0]], args[1]))
            else:
                pass

        for line in assembly:
            print(line)
