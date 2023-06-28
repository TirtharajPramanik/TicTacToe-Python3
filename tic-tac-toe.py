debug = False
autofill_lastmove = True

print("\x1B[0m")

matrix = [[str(col) for col in range(row, row + 3)] for row in [1, 4, 7]]


def evaluate_line(val, to_cmp):
    count = 0
    val_ = val
    while val_ > 0:
        val_ -= 1
        count += 1 if to_cmp(val_) == mark else 0
    val_ = val
    while val_ < 2:
        val_ += 1
        count += 1 if to_cmp(val_) == mark else 0
    return count == 2


def evaluate_diagonal(row, col, rtl=False):
    count = 0
    if rtl:
        row_ = row - 1
        col_ = col + 1
    else:
        row_ = row - 1
        col_ = col - 1
    while row_ >= 0 and row_ <= 2 and col_ >= 0 and col_ <= 2:
        count += 1 if matrix[row_][col_] == mark else 0
        if rtl:
            row_ -= 1
            col_ += 1
        else:
            row_ -= 1
            col_ -= 1
    if rtl:
        row_ = row + 1
        col_ = col - 1
    else:
        row_ = row + 1
        col_ = col + 1
    while row_ >= 0 and row_ <= 2 and col_ >= 0 and col_ <= 2:
        count += 1 if matrix[row_][col_] == mark else 0
        if rtl:
            row_ += 1
            col_ -= 1
        else:
            row_ += 1
            col_ += 1
    return count == 2


def evaluate(row, col):
    return (  # horizontal
        evaluate_line(col, lambda val: matrix[row][val])
        or
        # vertical
        evaluate_line(row, lambda val: matrix[val][col])
        or
        # ltr diagonal
        evaluate_diagonal(row, col, rtl=False)
        or
        # rtl diagonal
        evaluate_diagonal(row, col, rtl=True)
    )


clear = (
    lambda lines: print(f"\x1B[{lines}F", end="") if not debug else lambda lines: None
)

out = (
    lambda val: "\x1B[31m" + val + "\x1B[39m"
    if val == "X"
    else "\x1B[34m" + val + "\x1B[39m"
    if val == "O"
    else val
)


def show_board():
    print("\x1B[1m", end="")
    for row in matrix:
        lin = out(row[0]) + " | " + out(row[1]) + " | " + out(row[2])
        print(lin)
    print("\x1B[22m", end="")


errors = 0
move = 1


def next_gen():
    global errors, move
    lines = 4 + errors
    errors = 0
    move += 1
    clear(lines)
    show_board()


def gameover(mark=None):
    next_gen()
    print("Game Over,", out(mark), "wins", "\x1B[0J" if not debug else "")
    from sys import exit

    exit(0)


def warn(*msg, lines=1):
    global errors
    errors += 1
    clear(lines)
    print(*msg)


loc = lambda pos: ((pos - 1) // 3, (pos - 1) % 3)

if autofill_lastmove:

    def find_move():
        for row in matrix:
            for col in row:
                if col not in ["X", "O"]:
                    return loc(int(col))
        raise IndexError("no empty locations, after only", move, "moves")

    def evaluate_last_move():
        if move == 8:
            row, col = find_move()
            global mark
            mark = "X"
            matrix[row][col] = mark
            gameover(mark if evaluate(row, col) else "nobody")

else:

    def evaluate_last_move():
        if move == 9:
            gameover(mark if evaluate(row, col) else "nobody")


# start
show_board()

# update
while True:
    for mark in ["X", "O"]:
        while True:
            try:
                pos = int(input(out(mark) + " :- \x1B[0J"))
            except ValueError:
                warn("input is invalid")
                continue
            if pos <= 9 and pos >= 1:
                row, col = loc(pos)
                if matrix[row][col] == str(pos):
                    matrix[row][col] = mark
                    if move > 4:
                        if evaluate(row, col):
                            gameover(mark)
                        evaluate_last_move()
                    break
                else:
                    warn(pos, "is occupied")
            else:
                warn(pos, "does not exist")
        next_gen()
