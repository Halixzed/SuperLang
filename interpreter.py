from tokens import *

class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.globals = {}
        self.functions = {}

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        if self.pos >= len(self.tokens):
            raise Exception("Unexpected end of input.")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def match(self, expected_type):
        if self.peek() and self.peek().type == expected_type:
            return self.consume()
        return None

    def program(self):
        while self.pos < len(self.tokens):
            token = self.peek()
            if token and token.type == SEMICOLON:
                self.consume()
                continue
            result = self.statement()
            if isinstance(result, dict) and result.get('return', False):
                break

    def statement(self):
        token = self.peek()
        if token and token.type == SEMICOLON:
            self.consume()
            return None
        if token and token.type == FUNC:
            return self.function_definition()
        if token and token.type == IF:
            return self.if_statement()
        if token and token.type == WHILE:
            return self.while_statement()
        if token and token.type == IDENTIFIER:
            var_token = self.consume()
            if self.match(ASSIGN):
                value = self.expression()
                self.globals[var_token.value] = value
                return value
            else:
                self.pos -= 1
        if token and token.type == RETURN:
            self.consume()
            value = self.expression()
            return {'return': True, 'value': value}
        elif token and token.type == SAY:
            self.consume()
            value = self.expression()
            print(value)
            return None
        return self.expression()

    def function_definition(self):
        self.consume()  # consume FUNC
        name_token = self.consume()
        if name_token.type != IDENTIFIER:
            raise Exception("Expected function name after 'func'")
        func_name = name_token.value
        if not self.match(LPAREN):
            raise Exception("Expected '(' after function name")
        params = []
        while self.peek() and self.peek().type != RPAREN:
            param_token = self.consume()
            if param_token.type != IDENTIFIER:
                raise Exception("Expected parameter name")
            params.append(param_token.value)
            if self.peek() and self.peek().type == COMMA:
                self.consume()
        if not self.match(RPAREN):
            raise Exception("Expected ')' after parameters")
        if not self.match(LBRACE):
            raise Exception("Expected '{' to start function body")
        body_start = self.pos
        brace_count = 1
        while brace_count > 0 and self.pos < len(self.tokens):
            if self.tokens[self.pos].type == LBRACE:
                brace_count += 1
            elif self.tokens[self.pos].type == RBRACE:
                brace_count -= 1
            self.pos += 1
        body_end = self.pos - 1
        self.functions[func_name] = (params, body_start, body_end)
        return None

    def call_function(self, name, args):
        if name not in self.functions:
            raise Exception(f"Undefined function '{name}'")
        params, body_start, body_end = self.functions[name]
        if len(args) != len(params):
            raise Exception(f"Function '{name}' expects {len(params)} arguments")
        saved_pos = self.pos
        saved_globals = self.globals.copy()
        self.pos = body_start
        for i, param in enumerate(params):
            self.globals[param] = args[i]
        ret = None
        while self.pos < body_end:
            result = self.statement()
            if isinstance(result, dict) and result.get('return', False):
                ret = result['value']
                break
        self.globals = saved_globals
        self.pos = saved_pos
        return ret

    def expression(self):
        return self.parse_binary(0)

    PRECEDENCE = {
        OR: 1,
        AND: 2,
        EQ: 3, NEQ: 3, LT: 3, GT: 3,
        PLUS: 4, MINUS: 4,
        MUL: 5, DIV: 5,
    }

    def parse_binary(self, min_prec):
        left = self.unary()
        while True:
            op_token = self.peek()
            if op_token and op_token.type in self.PRECEDENCE and self.PRECEDENCE[op_token.type] >= min_prec:
                prec = self.PRECEDENCE[op_token.type]
                self.consume()
                right = self.parse_binary(prec + 1)
                if op_token.type == PLUS:
                    left = left + right
                elif op_token.type == MINUS:
                    left = left - right
                elif op_token.type == MUL:
                    left = left * right
                elif op_token.type == DIV:
                    left = left / right
                elif op_token.type == EQ:
                    left = left == right
                elif op_token.type == NEQ:
                    left = left != right
                elif op_token.type == LT:
                    left = left < right
                elif op_token.type == GT:
                    left = left > right
                elif op_token.type == AND:
                    left = left and right
                elif op_token.type == OR:
                    left = left or right
                else:
                    raise Exception(f"Unknown operator: {op_token.type}")
            else:
                break
        return left

    def unary(self):
        if self.peek() and self.peek().type == NOT:
            self.consume()
            return not self.unary()
        elif self.peek() and self.peek().type == MINUS:
            self.consume()
            return -self.unary()
        else:
            return self.primary()

    def primary(self):
        token = self.peek()
        if token is None:
            raise Exception("Expected value but got end of input.")
        if token.type in (NUMBER, BOOL, STRING):
            value = self.consume().value
        elif token.type == IDENTIFIER:
            name = self.consume().value
            if self.peek() and self.peek().type == LPAREN:
                self.consume()
                args = []
                while self.peek() and self.peek().type != RPAREN:
                    args.append(self.expression())
                    if self.peek() and self.peek().type == COMMA:
                        self.consume()
                if not self.match(RPAREN):
                    raise Exception("Expected ')' after arguments")
                return self.call_function(name, args)
            elif name in self.globals:
                value = self.globals[name]
            else:
                raise Exception(f"Undefined variable '{name}'")
        elif token.type == LPAREN:
            self.consume()
            value = self.expression()
            if not self.match(RPAREN):
                raise Exception("Missing closing parenthesis.")
        elif token.type == LBRACKET:
            self.consume()
            elements = []
            while self.peek() and self.peek().type != RBRACKET:
                elements.append(self.expression())
                if self.peek() and self.peek().type == COMMA:
                    self.consume()
            if not self.match(RBRACKET):
                raise Exception("Missing closing bracket for list.")
            value = elements
        elif token.type == LBRACE:
            self.consume()
            dct = {}
            while self.peek() and self.peek().type != RBRACE:
                key_token = self.consume()
                if key_token.type == STRING:
                    key = key_token.value
                elif key_token.type == IDENTIFIER:
                    key = key_token.value
                else:
                    raise Exception("Dictionary keys must be strings or identifiers.")
                if not self.match(COLON):
                    raise Exception("Expected ':' after dictionary key.")
                val = self.expression()
                dct[key] = val
                if self.peek() and self.peek().type == COMMA:
                    self.consume()
            if not self.match(RBRACE):
                raise Exception("Missing closing brace for dictionary.")
            value = dct
        else:
            raise Exception(f"Unexpected token: {token}")

        while self.peek() and self.peek().type == LBRACKET:
            self.consume()
            index = self.expression()
            if not self.match(RBRACKET):
                raise Exception("Missing closing bracket for index.")
            value = value[index]
        return value

    def if_statement(self):
        self.consume()  # consume IF
        if not self.match(LPAREN):
            raise Exception("Expected '(' after 'if'")
        condition = self.expression()
        if not self.match(RPAREN):
            raise Exception("Expected ')' after condition")
        if not self.match(LBRACE):
            raise Exception("Expected '{' to start if block")
        if_block_start = self.pos
        brace_count = 1
        while brace_count > 0 and self.pos < len(self.tokens):
            if self.tokens[self.pos].type == LBRACE:
                brace_count += 1
            elif self.tokens[self.pos].type == RBRACE:
                brace_count -= 1
            self.pos += 1
        if_block_end = self.pos - 1
        else_block_start = else_block_end = None
        if self.peek() and self.peek().type == ELSE:
            self.consume()
            if not self.match(LBRACE):
                raise Exception("Expected '{' to start else block")
            else_block_start = self.pos
            brace_count = 1
            while brace_count > 0 and self.pos < len(self.tokens):
                if self.tokens[self.pos].type == LBRACE:
                    brace_count += 1
                elif self.tokens[self.pos].type == RBRACE:
                    brace_count -= 1
                self.pos += 1
            else_block_end = self.pos - 1
        if condition:
            saved_pos = self.pos
            self.pos = if_block_start
            while self.pos < if_block_end:
                self.statement()
            self.pos = saved_pos
        elif else_block_start is not None:
            saved_pos = self.pos
            self.pos = else_block_start
            while self.pos < else_block_end:
                self.statement()
            self.pos = saved_pos
        return None

    def while_statement(self):
        self.consume()  # consume WHILE
        if not self.match(LPAREN):
            raise Exception("Expected '(' after 'while'")
        condition_start = self.pos
        condition = self.expression()
        if not self.match(RPAREN):
            raise Exception("Expected ')' after condition")
        if not self.match(LBRACE):
            raise Exception("Expected '{' to start while block")
        block_start = self.pos
        brace_count = 1
        while brace_count > 0 and self.pos < len(self.tokens):
            if self.tokens[self.pos].type == LBRACE:
                brace_count += 1
            elif self.tokens[self.pos].type == RBRACE:
                brace_count -= 1
            self.pos += 1
        block_end = self.pos - 1

        while True:
            saved_pos = self.pos
            self.pos = condition_start
            cond = self.expression()
            self.pos = saved_pos
            if not cond:
                break
            saved_pos = self.pos
            self.pos = block_start
            while self.pos < block_end:
                self.statement()
            self.pos = saved_pos
        return None