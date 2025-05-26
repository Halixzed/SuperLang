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

say "Stage 6: Lists";
mylist = {1, 2, 3, 4};
say mylist;
say mylist[2];

func first(lst) {
    return lst[0];
}
say first({99, 100});

say "Stage 6: Dictionaries";
mydict = ["a": 10, "b": 20];
say mydict;
say mydict["b"];

func getval(d, k) {
    return d[k];
}
say getval(["x": 42], "x");
