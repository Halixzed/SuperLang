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
        globals_state = {}
        while True:
            try:
                source = input("SuperLang (⌐■_■) > ")
                # Ignore empty input
                if not source.strip():
                    continue
                # Exit condition
                if source.strip().lower() in ("exit", "quit"):
                    break

                # Tokenize and interpret the current input
                lexer = Lexer(source)
                tokens = lexer.tokenize()
                interpreter = Interpreter(tokens)

                # Restore global state only
                interpreter.globals = globals_state.copy()

                # Run the program
                interpreter.program()

                # Save global state for the next input
                globals_state = interpreter.globals.copy()

            except Exception as e:
                print("Error:", e)