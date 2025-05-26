from time import sleep
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
                # Replace Unicode minus (en dash/em dash) with ASCII minus
                source = source.replace("–", "-").replace("—", "-")
                # Ignore empty input
                if not source.strip():
                    continue
                # Exit condition
                if source.strip().lower() in ("exit", "quit"):
                    print("Exiting SuperLang. Stay frosty (⌐■_■)!")
                    sleep(1)
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