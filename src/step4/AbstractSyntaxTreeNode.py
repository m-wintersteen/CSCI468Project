L_VALUE = 0
R_VALUE = 1

t = 0

def getTemp():
    global t
    t = t + 1
    return '$T{}'.format(t)


class AbstractSyntaxTreeNode:

    def __init__(self):
        self.left = None
        self.right = None
        self.temp = None
        self.type = None
        self.varType = None
    
    def generateCode(self):
        pass

    
class AssignmentNode(AbstractSyntaxTreeNode):

    def __init__(self):
        super().__init__()

    def generateCode(self):
        code = self.right.generateCode()
        instruction = None
        if self.right.varType == 'FLOAT':
            instruction = 'STOREF'
        else:
            instruction = 'STOREI'
        if isinstance(self.right, LiteralNode):
            temp = getTemp()
            code.append(';{} {} {}'.format(instruction, self.right.temp, temp))
            code.append(';{} {} {}'.format(instruction, temp, self.left.temp))
        else:
            code.append(';{} {} {}'.format(instruction, self.right.temp, self.left.temp))
        return code


class IdentifierNode(AbstractSyntaxTreeNode):
    
    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.type = L_VALUE
        self.varType = 'INT'

    def generateCode(self):
        return []


class OperatorNode(AbstractSyntaxTreeNode):
    
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        self.type = R_VALUE

    def generateCode(self):
        code = self.left.generateCode() + self.right.generateCode()
        self.temp = getTemp()
        instruction = None
        if self.operator == '+':
            instruction = 'ADDI'
        elif self.operator == '-':
            instruction = 'SUBI'
        elif self.operator == '*':
            instruction = 'MULTI'
        elif self.operator == '/':
            instruction = 'DIVI'
        templ = self.left.temp
        tempr = self.right.temp
        if isinstance(self.left, LiteralNode):
            templ = getTemp()
            code.append(';STOREI {} {}'.format(self.left.temp, templ))
        if isinstance(self.right, LiteralNode):
            tempr = getTemp()
            code.append(';STOREI {} {}'.format(self.right.temp, tempr))
        code.append(';{} {} {} {}'.format(instruction, templ, tempr, self.temp))
        return code


class LiteralNode(AbstractSyntaxTreeNode):

    def __init__(self, temp):
        super().__init__()
        self.temp = temp
        self.type = R_VALUE
        self.varType = 'INT'

    def generateCode(self):
        return []


class WriteNode(AbstractSyntaxTreeNode):
    def __init__(self):
        super().__init__()
        self.type = None

    def generateCode(self):
        instruction = 'WRITE' + 'I' if self.left.varType == 'INT' else 'F'
        return ['{} {}'.format(instruction, self.left.temp)]

