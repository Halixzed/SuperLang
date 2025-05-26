say "Stage 5: Control flow";
i = 0;
sum = 0;
while (i < 5) {
    sum = sum + i;
    i = i + 1;
}
say sum;

// Limited loop for shopping list
is_running = true;
shopping_list = "";
count = 0;
while (is_running == true) {
    item = "apple";
    if (count == 2) {
        is_running = false;
    }
    shopping_list = shopping_list + ", " + item;
    count = count + 1;
}
say shopping_list;
