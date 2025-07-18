import curses
import random


def main(stdscr):
    # Initialize screen
    curses.curs_set(0)
    curses.start_color()
    sh, sw = stdscr.getmaxyx()

    # Define play area
    margin = 2
    play_height = min(25, sh - margin * 2)
    play_width = min(50, (sw // 2) - margin * 2)

    # Colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)  # Food
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Border

    # Main game window
    win = curses.newwin(play_height, play_width, margin, margin)
    win.keypad(1)
    win.timeout(100)
    win.border()
    win.bkgd(' ', curses.color_pair(3))

    # Control message
    try:
        controls = curses.newwin(1, sw, sh - 1, 0)
        controls.addstr(0, 0, " CONTROL: Arrow Keys (↑ ↓ ← →) ONLY ", curses.A_REVERSE)
        controls.refresh()
    except:
        pass

    # Initial snake
    snake = [[play_height // 2, play_width // 2 - i] for i in range(3)]
    for y, x in snake:
        win.addch(y, x, '■', curses.color_pair(2))

    # First food
    food = [random.randint(1, play_height - 2), random.randint(1, play_width - 2)]
    win.addch(food[0], food[1], '●', curses.color_pair(1))

    # Game variables
    score = 0
    snake_length = len(snake)  # Track snake length
    direction = curses.KEY_RIGHT

    while True:
        # Display score and length (centered at top)
        info_str = f" SCORE: {score} | LENGTH: {snake_length} "
        win.addstr(0, (play_width - len(info_str)) // 2, info_str, curses.color_pair(3))

        # Handle input
        next_key = win.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if not (direction == curses.KEY_UP and next_key == curses.KEY_DOWN or
                    direction == curses.KEY_DOWN and next_key == curses.KEY_UP or
                    direction == curses.KEY_LEFT and next_key == curses.KEY_RIGHT or
                    direction == curses.KEY_RIGHT and next_key == curses.KEY_LEFT):
                direction = next_key

        # Move snake
        head = snake[0].copy()
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        # Check collisions
        if (head[0] in [0, play_height - 1] or
                head[1] in [0, play_width - 1] or
                head in snake):
            break

        # Update snake
        snake.insert(0, head)
        snake_length = len(snake)  # Update length counter
        win.addch(head[0], head[1], '■', curses.color_pair(2))

        # Food check
        if head == food:
            score += 10
            food = None
            while not food:
                nf = [
                    random.randint(1, play_height - 2),
                    random.randint(1, play_width - 2)
                ]
                food = nf if nf not in snake else None
            win.addch(food[0], food[1], '●', curses.color_pair(1))
        else:
            tail = snake.pop()
            snake_length = len(snake)  # Update length when moving
            win.addch(tail[0], tail[1], ' ')

    # Game Over
    win.addstr(play_height // 2, play_width // 2 - 5, 'GAME OVER')
    win.addstr(play_height // 2 + 1, play_width // 2 - 10, f'FINAL SCORE: {score} | LENGTH: {snake_length}')
    win.refresh()
    curses.beep()
    curses.napms(2000)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except:
        pass
    finally:
        print("\nThanks for playing! Controls: Arrow keys only")
