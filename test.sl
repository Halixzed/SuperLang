// Stage 1: Arithmetic
say "Stage 1: Arithmetic";
say 1 - 2;
say 2.5 + 2.5 - 1.25;
say (10 * 2) / 6;
say 8.5 / (2 * 9) - -3;

// Stage 2: Boolean logic
say "Stage 2: Boolean logic";
say true == false;
say true != false;
say (5 < 10);
say !(5 - 4 > 3 * 2 == !false);
say true and true;
say false and true;
say (0 < 1) or false;
say false or false;

// Stage 3: Strings
say "Stage 3: Strings";
say "hello" + " " + "world";
say "foo" + "bar" == "foobar";
say "10 corgis" != "10" + "corgis";

// Stage 4: Global variables
say "Stage 4: Global variables";
quickMaths = 10;
quickMaths = quickMaths + 2;
say quickMaths;
floatTest = 1.0;
floatTest = floatTest + 5;
say floatTest;
stringCatTest = "10 corgis";
stringCatTest = stringCatTest + 5 + " more corgis";
say stringCatTest;
errorTest = 5;
errorTest = errorTest + "insert string here";
say errorTest;

// Stage 5: Control flow
say "Stage 5: Control flow";
i = 0;
sum = 0;
while (i < 5) {
    sum = sum + i;
    i = i + 1;
}
say sum;

// Fix infinite loop: add a counter to limit iterations
is_running = true;
shopping_list = "";
count = 0;
while (is_running == true) {
    item = "apple"; // replace with input("add an item to the shopping list: ") if input is supported
    if (count == 2) { // stop after 2 items
        is_running = false;
    }
    shopping_list = shopping_list + ", " + item;
    count = count + 1;
}
say shopping_list;

// Stage 6: Functions
say "Stage 6: Functions";
func add(a, b) {
    result = a + b;
    return result;
}
say add(2, 3);

func greet() {
    say "Hello from greet!";
}
greet();

func square(x) {
    y = x * x;
    return y;
}
say square(4);

func double(x) {
    return x + x;
}
say double(add(2, 5));

func abs(x) {
    if (x < 0) {
        return -x;
    } else {
        return x;
    }
}
say abs(-10);
say abs(7);

func sum_to_n(n) {
    total = 0;
    i = 1;
    while (i <= n) {
        total = total + i;
        i = i + 1;
    }
    return total;
}
say sum_to_n(5);

func nop() {
    x = 1;
}
say nop();

// Stage 6: Lists
say "Stage 6: Lists";
mylist = {1, 2, 3, 4};
say mylist;
say mylist[2];

func first(lst) {
    return lst[0];
}
say first({99, 100});

// Stage 6: Dictionaries
say "Stage 6: Dictionaries";
mydict = ["a": 10, "b": 20];
say mydict;
say mydict["b"];

func getval(d, k) {
    return d[k];
}
say getval(["x": 42], "x");
