from tokens import *

class Interpreter:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.globals = {}
        self.functions = {}  # Add back function storage

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
            try:
                result = self.statement()
                if result is not None:
                    print(result)
            except Exception as e:
                print(f"Error: {e}")

    def statement(self, local_vars=None):
        token = self.peek()
        if token and token.type == SEMICOLON:
            self.consume()
            return None
        # stray commas etcv 
        # if token and token.type == COMMA:
        #     self.consume()
        #     return None
        # if token and token.type == RBRACE:
        #     self.consume()
        #     return None
        # if token and token.type == RBRACKET:
        #     self.consume()
        #     return None
        if token and token.type == FUNC:
            return self.function_definition()
        if token and token.type == RETURN:
            self.consume()
            value = self.expression(local_vars)
            return {'return': True, 'value': value}
        if token and token.type == IDENTIFIER:
            var_token = self.consume()
            if self.peek() and self.peek().type == ASSIGN:
                self.consume()
                value = self.expression(local_vars)
                if local_vars is not None:
                    local_vars[var_token.value] = value
                else:
                    self.globals[var_token.value] = value
                return None
            else:
                self.pos -= 1
        if token and token.type == SAY:
            self.consume()
            value = self.expression(local_vars)
            print(value)
            return None
        if token and token.type == IF:
            return self.if_statement(local_vars)
        if token and token.type == WHILE:
            return self.while_statement(local_vars)
        return self.expression(local_vars)

    def function_definition(self):
        self.consume()  # consume 'func'
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
            raise Exception(f"Function '{name}' expects {len(params)} arguments, got {len(args)}")
        saved_pos = self.pos
        local_vars = dict(zip(params, args))
        self.pos = body_start
        ret = None
        while self.pos < body_end:
            result = self.statement(local_vars)
            if isinstance(result, dict) and result.get('return', False):
                ret = result['value']
                break
        self.pos = saved_pos
        return ret

    # Operator precedence for all supported operators
    PRECEDENCE = {
        OR: 1,
        AND: 2,
        EQ: 3, NEQ: 3, LT: 3, GT: 3,
        PLUS: 4, MINUS: 4,
        MUL: 5, DIV: 5,
    }

    def expression(self, local_vars=None):
        return self.parse_binary(0, local_vars)

    def parse_binary(self, min_prec, local_vars=None):
        left = self.unary(local_vars)
        while True:
            op_token = self.peek()
            if op_token and op_token.type in self.PRECEDENCE and self.PRECEDENCE[op_token.type] >= min_prec:
                prec = self.PRECEDENCE[op_token.type]
                self.consume()
                right = self.parse_binary(prec + 1, local_vars)
                left = self.apply_operator(op_token.type, left, right)
            else:
                break
        return left

    def apply_operator(self, op_type, left, right):
        # Arithmetic
        if op_type == PLUS:
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        elif op_type == MINUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left - right
            raise Exception("Invalid types for '-'")
        elif op_type == MUL:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left * right
            raise Exception("Invalid types for '*'")
        elif op_type == DIV:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left / right
            raise Exception("Invalid types for '/'")
        # Boolean logic
        elif op_type == EQ:
            return left == right
        elif op_type == NEQ:
            return left != right
        elif op_type == LT:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left < right
            raise Exception("Invalid types for '<'")
        elif op_type == GT:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left > right
            raise Exception("Invalid types for '>'")
        elif op_type == AND:
            if isinstance(left, bool) and isinstance(right, bool):
                return left and right
            raise Exception("Invalid types for 'and'")
        elif op_type == OR:
            if isinstance(left, bool) and isinstance(right, bool):
                return left or right
            raise Exception("Invalid types for 'or'")
        else:
            raise Exception(f"Unexpected operator: {op_type}")

    def unary(self, local_vars=None):
        if self.peek() and self.peek().type == NOT:
            self.consume()
            value = self.unary(local_vars)
            if not isinstance(value, bool):
                raise Exception("Unary '!' only valid for booleans")
            return not value
        elif self.peek() and self.peek().type == MINUS:
            self.consume()
            value = self.unary(local_vars)
            if not isinstance(value, (int, float)):
                raise Exception("Unary '-' only valid for numbers")
            return -value
        else:
            return self.primary(local_vars)

    def primary(self, local_vars=None):
        token = self.peek()
        if token is None:
            raise Exception("Expected value but got end of input.")
        elif token.type == NUMBER:
            # Return int for NUMBER, float for FLOAT
            return int(self.consume().value)
        elif token.type == FLOAT:
            return float(self.consume().value)
        elif token.type == BOOL:
            val = self.consume().value
            if val == "true":
                return True
            elif val == "false":
                return False
            else:
                raise Exception(f"Invalid boolean value: {val}")
        elif token.type == STRING:
            return self.consume().value
        elif token.type == IDENTIFIER:
            name = self.consume().value
            # Built-in function: select_sample()
            if name == "select_sample" and self.peek() and self.peek().type == LPAREN:
                self.consume()  # consume '('
                if not self.match(RPAREN):
                    raise Exception("select_sample() takes no arguments")
                self.run_sample_selector()
                return None
            if self.peek() and self.peek().type == LPAREN:
                self.consume()
                args = []
                while self.peek() and self.peek().type != RPAREN:
                    args.append(self.expression(local_vars))
                    if self.peek() and self.peek().type == COMMA:
                        self.consume()
                if not self.match(RPAREN):
                    raise Exception("Expected ')' after arguments")
                return self.call_function(name, args)
            elif local_vars is not None and name in local_vars:
                value = local_vars[name]
            elif name in self.globals:
                value = self.globals[name]
            else:
                raise Exception(f"Undefined variable '{name}'")
            # Support indexing: mylist[2] or mydict["b"]
            while self.peek() and self.peek().type == LBRACKET:
                self.consume()
                index = self.expression(local_vars)
                if isinstance(value, list):
                    # Convert float/int index to int for lists
                    if not isinstance(index, int):
                        if isinstance(index, float) and index.is_integer():
                            index = int(index)
                        else:
                            raise Exception("List indices must be integers")
                if not self.match(RBRACKET):
                    raise Exception("Missing closing bracket for index.")
                value = value[index]
            return value
        elif token.type == LPAREN:
            self.consume()
            value = self.expression(local_vars)
            if not self.match(RPAREN):
                raise Exception("Missing closing parenthesis.")
            return value
        elif token.type == LBRACE:
            # List literal: {1, 2, 3}
            self.consume()
            elements = []
            while self.peek() and self.peek().type != RBRACE:
                elements.append(self.expression(local_vars))
                if self.peek() and self.peek().type == COMMA:
                    self.consume()
            if not self.match(RBRACE):
                raise Exception("Missing closing brace for list.")
            return elements

        elif token.type == LBRACKET:
            # Dictionary literal: ["a": 1, "b": 2]
            self.consume()
            d = {}
            while self.peek() and self.peek().type != RBRACKET:
                key = self.expression(local_vars)
                if not self.match(COLON):
                    raise Exception("Expected ':' in dictionary")
                value = self.expression(local_vars)
                d[key] = value
                if self.peek() and self.peek().type == COMMA:
                    self.consume()
            if not self.match(RBRACKET):
                raise Exception("Missing closing bracket for dictionary.")
            return d

        # Fixing handling stray ASSIGN tokens (e.g. from malformed input)
        if token.type == ASSIGN:
            self.consume()
            # Skip and try to continue parsing
            return self.primary(local_vars)
        else:
            raise Exception(f"Unexpected token: {token}")

    def if_statement(self, local_vars=None):
        self.consume()
        if not self.match(LPAREN):
            raise Exception("Expected '(' after 'if'")
        condition = self.expression(local_vars)
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
                self.statement(local_vars)
            self.pos = saved_pos
        elif else_block_start is not None:
            saved_pos = self.pos
            self.pos = else_block_start
            while self.pos < else_block_end:
                self.statement(local_vars)
            self.pos = saved_pos
        return None

    def while_statement(self, local_vars=None):
        self.consume()
        if not self.match(LPAREN):
            raise Exception("Expected '(' after 'while'")
        condition_start = self.pos
        saved_condition_pos = self.pos
        condition = self.expression(local_vars)
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
            self.pos = saved_condition_pos
            cond = self.expression(local_vars)
            self.pos = saved_pos
            if not cond:
                break
            saved_pos = self.pos
            self.pos = block_start
            while self.pos < block_end:
                self.statement(local_vars)
            self.pos = saved_pos
        return None

    def run_sample_selector(self):
        import os
        # Import Lexer and Interpreter here to ensure they are available
        from lexer import Lexer
        from interpreter import Interpreter
        samples_dir = os.path.join(os.path.dirname(__file__), "StageSamples")
        if not os.path.isdir(samples_dir):
            print("No StageSamples directory found.")
            return
        sample_files = [f for f in os.listdir(samples_dir) if f.endswith(".sl")]
        if not sample_files:
            print("No .sl sample files found in StageSamples.")
            return
        print("Sample .sl files in StageSamples:")
        for idx, fname in enumerate(sample_files):
            print(f"{idx+1}: {fname}")
        choice = input("Enter number to run a sample, or press Enter to cancel: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(sample_files):
            fname = sample_files[int(choice)-1]
            with open(os.path.join(samples_dir, fname), "r") as f:
                source = f.read()
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            interpreter = Interpreter(tokens)
            interpreter.program()
        else:
            print("No sample selected.")