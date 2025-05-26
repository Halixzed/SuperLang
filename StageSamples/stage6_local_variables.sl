say "Stage 6: Local Variables";

// Local variables inside a function should not affect globals
x = 100;
func test_local() {
    x = 5;
    y = 10;
    say x; // Should print 5 (local)
    say y; // Should print 10 (local)
}
test_local();
say x; // Should print 100 (global, unchanged)

// Local variable shadowing parameter
func shadow(a) {
    a = a + 10;
    say a; // Should print parameter + 10
}
shadow(7); // Should print 17

// Local variable does not leak between calls
func counter() {
    c = 0;
    c = c + 1;
    return c;
}
say counter(); // Should print 1
say counter(); // Should print 1 again

// No nested function test, as not supported
