import re


class Translator:

    def __init__(self):
        self.r = -1


    def toreg(self, temp):
        matches = re.match(r'\$T(\d+)', temp)
        if matches:
            return 'r{}'.format(int(matches.group(1)) - 1)
        else:
            return temp


    def translate(self, code, symbolTable):
        assembly = []
        regmap = {}
        for id in symbolTable:
            if symbolTable[id]['type'] == 'STRING':
                assembly.append('str {} {}'.format(id, symbolTable[id]['value']))
            else:
                assembly.append('var {}'.format(id))
        for line in code:
            [instr, *args] = line.split(' ')
            if len(args) == 3:
                op1 = self.toreg(args[0])
                op2 = self.toreg(args[1])
                dest = self.toreg(args[2])
                assembly.append('move {} {}'.format(op1, dest))
                assembly.append('{} {} {}'.format(instr.lower().replace('f', 'r').replace('t', ''), op2, dest))
            elif len(args) == 2:
                assembly.append('move {} {}'.format(self.toreg(args[0]), self.toreg(args[1])))
            else:
                assembly.append('sys {} {}'.format(instr.lower().replace('f', 'r'), args[0]))
        assembly.append('sys halt')

        return assembly
