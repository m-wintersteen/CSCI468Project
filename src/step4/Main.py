import sys
from antlr4 import *
from LittleLexer import LittleLexer
from LittleParser import LittleParser
from AbstractSyntaxTreeVisitor import AbstractSyntaxTreeVisitor
from SymbolTableVisitor import SymbolTableVisitor
from antlr4.error.ErrorListener import ConsoleErrorListener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = LittleLexer(input_stream)
    lexer.removeErrorListener(ConsoleErrorListener.INSTANCE)
    stream = CommonTokenStream(lexer)
    parser = LittleParser(stream)
    parser.removeErrorListener(ConsoleErrorListener.INSTANCE)
    tree = parser.program()
    visitor = SymbolTableVisitor()
    visitor.visit(tree)
    visitor = AbstractSyntaxTreeVisitor(visitor.symbolTable['GLOBAL'])
    visitor.visit(tree)

 
if __name__ == '__main__':
    main(sys.argv)