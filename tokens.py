# mytoken.py
NUMBER = 'NUMBER'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
BOOL = 'BOOL'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQ = 'EQ'
NEQ = 'NEQ'
LT = 'LT'
GT = 'GT'
STRING = 'STRING'
CONCAT = 'CONCAT'
IDENTIFIER = 'IDENTIFIER'
SAY = 'SAY'
ASSIGN = 'ASSIGN'
IF = 'IF'
ELSE = 'ELSE'
WHILE = 'WHILE'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
COMMA = 'COMMA'
COLON = 'COLON'
FUNC = 'FUNC'
RETURN = 'RETURN'
SEMICOLON = 'SEMICOLON'



class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'{self.type}:{self.value}'
