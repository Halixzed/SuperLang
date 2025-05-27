from lexer import Lexer
from interpreter import Interpreter
from time import sleep
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
        functions_state = {}
        while True:
            try:
                source = input("SuperLang (⌐■_■) > ")
                # Ignore empty input
                if not source.strip():
                    continue
                # Exit condition
                if source.strip().lower() in ("exit", "quit"):
                    print("Exiting SuperLang. Stay Frosty (⌐■_■)!")
                    sleep(1)
                    break

                # Tokenize and interpret the current input
                lexer = Lexer(source)
                tokens = lexer.tokenize()
                interpreter = Interpreter(tokens)

                # Restore global and function states
                interpreter.globals = globals_state.copy()
                interpreter.functions = functions_state.copy()

                # Run the program
                interpreter.program()

                # Save global and function states for the next input
                globals_state = interpreter.globals.copy()
                functions_state = interpreter.functions.copy()

            except Exception as e:
                print("Error:", e)