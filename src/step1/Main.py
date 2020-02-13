import sys
from antlr4 import *
from Little import Little
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = Little(input_stream)
    for token in lexer.getAllTokens():
        print('Token Type: ' + lexer.symbolicNames[token.type])
        print('Value: ' + token.text)
 
if __name__ == '__main__':
    main(sys.argv)