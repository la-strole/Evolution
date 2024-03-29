import sys, os
import curses
from curses import textpad

class Animal_Window:
    # animal
    def __init__(self, x, y):
        animal = curses.newwin(10, 18, y, x)
        a_max_y, a_max_x = animal.getmaxyx()
        animal.border()
        animal.addstr(1, 1, 'fat:')
        animal.addstr(2, 1, 'red:')
        animal.addstr(3, 1, 'blue:')
        animal.hline(4, 1, '-', a_max_x - 2)
        self.animal_window = animal
        #animal.refresh()
        #animal.getch()

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()

    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width - 1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height - 1, cursor_y)

        # Declaration of strings
        title = "Curses example"[:width - 1]
        subtitle = "Written by Clay McLeod"[:width - 1]
        keystr = "Last key pressed: {}".format(k)[:width - 1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width - 1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        whstr = "Width: {}, Height: {}".format(width, height)
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def box(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    stdscr.hline(2, 0, '=', sw)
    text = 'Development phase'
    stdscr.addstr(1, sw // 2 - len(text) // 2, text)
    stdscr.border()
    stdscr.refresh()
    # stdscr.getch()


    #animal = Animal_Window(3, 10)
    #animal.animal_window.refresh()
    #animal.animal_window.getch()

    animals = []
    x, y = 3, 10

    for i in range(5):
        animals.append(Animal_Window(x, y))
        animals[-1].animal_window.refresh()
        x += 20

    animals[-1].animal_window.getch()

def main():
    curses.wrapper(box)


if __name__ == "__main__":
    main()
