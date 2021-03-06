lexer grammar Little;

KEYWORD : 'PROGRAM' | 'BEGIN' | 'END' | 'FUNCTION' | 'READ' | 'WRITE' | 'IF' | 'ELSE' | 'ENDIF' | 'WHILE' | 'ENDWHILE' | 'CONTINUE' | 'BREAK' | 'RETURN' | 'INT' | 'VOID' | 'STRING' | 'FLOAT' ;
IDENTIFIER : [A-z]+([A-z]|[0-9])* ;
OPERATOR : ':=' | '+' | '-' | '*' | '/' | '=' | '!=' | '<' | '>' | '(' | ')' | ';' | ',' | '<=' | '>=' ;
INTLITERAL : [0-9]+ ;
FLOATLITERAL: [0-9]*'.'[0-9]+ ;
STRINGLITERAL: ('"'.*?'"') ;
COMMENT: '--'.*?'\n' -> skip ;
WS: [ \n\t\r]+ -> skip ;