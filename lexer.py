from tokens import *

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []

    def tokenize(self):
        i = 0
        while i < len(self.source):
            c = self.source[i]
            if c.isspace():
                i += 1
                continue
            # Skip single-line comments
            if c == '/' and i + 1 < len(self.source) and self.source[i + 1] == '/':
                while i < len(self.source) and self.source[i] != '\n':
                    i += 1
                continue
            if c.isdigit():
                num = c
                i += 1
                has_dot = False
                while i < len(self.source) and (self.source[i].isdigit() or (self.source[i] == '.' and not has_dot)):
                    if self.source[i] == '.':
                        has_dot = True
                    num += self.source[i]
                    i += 1
                if has_dot:
                    self.tokens.append(Token(FLOAT, float(num)))  # FLOAT token for floats
                else:
                    self.tokens.append(Token(NUMBER, int(num)))  # NUMBER token for integers
                continue
            if c == '#':
                # handling comments --- new feature
                while i < len(self.source) and self.source[i] != '\n':
                    i += 1
                continue
            if c.isalpha() or c == '_':
                ident = c
                i += 1
                while i < len(self.source) and (self.source[i].isalnum() or self.source[i] == '_'):
                    ident += self.source[i]
                    i += 1
                if ident == 'true' or ident == 'false':
                    # Store as string, not Python bool
                    self.tokens.append(Token(BOOL, ident))
                elif ident == 'and':
                    self.tokens.append(Token(AND, ident))
                elif ident == 'or':
                    self.tokens.append(Token(OR, ident))
                elif ident == 'not':
                    self.tokens.append(Token(NOT, ident))
                elif ident == 'say':
                    self.tokens.append(Token(SAY, ident))
                elif ident == 'if':
                    self.tokens.append(Token(IF, ident))
                elif ident == 'else':
                    self.tokens.append(Token(ELSE, ident))
                elif ident == 'while':
                    self.tokens.append(Token(WHILE, ident))
                elif ident == 'func':
                    self.tokens.append(Token(FUNC, ident))
                elif ident == 'return':
                    self.tokens.append(Token(RETURN, ident))
                else:
                    self.tokens.append(Token(IDENTIFIER, ident))
                continue
            if c == '+':
                self.tokens.append(Token(PLUS, c))
                i += 1
                continue
            if c == '-':
                self.tokens.append(Token(MINUS, c))
                i += 1
                continue
            if c == '*':
                self.tokens.append(Token(MUL, c))
                i += 1
                continue
            if c == '/':
                self.tokens.append(Token(DIV, c))
                i += 1
                continue
            if c == '(':
                self.tokens.append(Token(LPAREN, c))
                i += 1
                continue
            if c == ')':
                self.tokens.append(Token(RPAREN, c))
                i += 1
                continue
            if c == '{':
                self.tokens.append(Token(LBRACE, c))
                i += 1
                continue
            if c == '}':
                self.tokens.append(Token(RBRACE, c))
                i += 1
                continue
            if c == '[':
                self.tokens.append(Token(LBRACKET, c))
                i += 1
                continue
            if c == ']':
                self.tokens.append(Token(RBRACKET, c))
                i += 1
                continue
            if c == ',':
                self.tokens.append(Token(COMMA, c))
                i += 1
                continue
            if c == ':':
                self.tokens.append(Token(COLON, c))
                i += 1
                continue
            if c == '=':
                if i + 1 < len(self.source) and self.source[i + 1] == '=':
                    self.tokens.append(Token(EQ, '=='))
                    i += 2
                else:
                    self.tokens.append(Token(ASSIGN, c))
                    i += 1
                continue
            if c == '!':
                if i + 1 < len(self.source) and self.source[i + 1] == '=':
                    self.tokens.append(Token(NEQ, '!='))
                    i += 2
                else:
                    self.tokens.append(Token(NOT, c))
                    i += 1
                continue
            if c == '<':
                self.tokens.append(Token(LT, c))
                i += 1
                continue
            if c == '>':
                self.tokens.append(Token(GT, c))
                i += 1
                continue
            if c == '"':
                i += 1
                s = ''
                while i < len(self.source) and self.source[i] != '"':
                    s += self.source[i]
                    i += 1
                i += 1  # skip closing quote
                self.tokens.append(Token(STRING, s))
                continue
            if c == ';':
                self.tokens.append(Token(SEMICOLON, c))
                i += 1
                continue
            raise Exception(f"Unknown character: {c}")
        return self.tokens