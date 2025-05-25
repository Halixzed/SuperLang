from lexer import Lexer
from interpreter import Interpreter
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        interpreter = Interpreter(tokens)
        interpreter.program()
    else:
        source_lines = []
        globals_state = {}
        while True:
            try:
                source = input("SuperLang (⌐■_■) > ")
                if source.strip().lower() in ("exit", "quit"):
                    break
                source_lines.append(source)
                if len(source_lines) > 1:
                    setup_source = "\n".join(source_lines[:-1])
                    setup_lexer = Lexer(setup_source)
                    setup_tokens = setup_lexer.tokenize()
                    setup_interpreter = Interpreter(setup_tokens)
                    setup_interpreter.program()
                    globals_state = setup_interpreter.globals.copy()
                else:
                    globals_state = {}
                last_line = source_lines[-1]
                lexer = Lexer(last_line)
                tokens = lexer.tokenize()
                interpreter = Interpreter(tokens)
                interpreter.globals = globals_state.copy()
                if len(source_lines) > 1:
                    interpreter.functions = setup_interpreter.functions.copy()
                interpreter.program()
            except Exception as e:
                print("Error:", e)