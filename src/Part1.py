import sys
from antlr4 import *
from antlr.LittleLexer import LittleLexer
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = LittleLexer(input_stream)
 
if __name__ == '__main__':
    main(sys.argv)