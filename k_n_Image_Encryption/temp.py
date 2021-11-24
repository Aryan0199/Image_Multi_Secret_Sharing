import os
from simple_term_menu import TerminalMenu


def main():
    flag = True
    while flag:
        options = os.listdir(os.getcwd())
        # options = ["entry 1", "entry 2", "entry 3"]
        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        if options[menu_entry_index].endswith(('.png', '.jpg', '.jpeg', '.tiff')):
            print(f"You have the image: {options[menu_entry_index]}!")
            flag = False


if __name__ == "__main__":
    main()
