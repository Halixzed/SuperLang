SuperLang
=========

SuperLang is a simple, dynamically-typed scripting language designed for learning and experimentation.  
*This was made as part of the academic coursework for Language Design and Implementation module.*

---

Features
--------

- **Arithmetic:** `+`, `-`, `*`, `/`, parentheses, unary negation
- **Booleans:** `true`, `false`, `==`, `!=`, `<`, `>`, `and`, `or`, `!`
- **Strings:** Double-quoted, concatenation with `+`, equality/inequality
- **Variables:** Global and local (in functions)
- **Output:** `say` statement prints to console
- **Control Flow:** `if`, `else`, `while` (with nesting)
- **Functions:** `func` keyword, parameters, return values, local scope
- **Lists:** `{1, 2, 3}`, index with `[i]`
- **Dictionaries:** `["key": value, ...]`, lookup with `["key"]`
- **Comments:** `//` or `#` for single-line comments
- **Semicolons:** `;` to separate statements

---

Example
-------

```sl
// Arithmetic and variables
x = 10;
y = 2.5;
say x + y * 2;

// Booleans and control flow
if (x > y) {
    say "x is greater";
} else {
    say "y is greater or equal";
}

// Functions
func add(a, b) {
    return a + b;
}
say add(3, 4);

// Lists and dictionaries
mylist = {1, 2, 3};
say mylist[1]; // prints 2

mydict = ["foo": 42, "bar": 99];
say mydict["bar"]; // prints 99
```

---

Running SuperLang
-----------------

To run a SuperLang script:

    python main.py yourscript.sl

Or use the interactive REPL:

    python main.py

---

Language Reference
------------------

### Data Types

- **Numbers:** `1`, `2.5`, `-3`
- **Booleans:** `true`, `false`
- **Strings:** `"hello world"`
- **Lists:** `{1, 2, 3}`
- **Dictionaries:** `["a": 1, "b": 2]`

### Statements

- **Assignment:** `x = 5;`
- **Output:** `say x + 1;`
- **If:**  
      if (x > 0) { say "positive"; } else { say "not positive"; }
- **While:**  
      i = 0;
      while (i < 3) { say i; i = i + 1; }
- **Function:**  
      func square(n) { return n * n; }
      say square(5);

### Lists and Dictionaries

- **List:**  
      nums = {1, 2, 3};
      say nums[0]; // 1
- **Dictionary:**  
      d = ["foo": 10, "bar": 20];
      say d["foo"]; // 10

---

Example Test File
-----------------

See `test.sl` for a comprehensive set of language features and tests.

---

License
-------

MIT License
