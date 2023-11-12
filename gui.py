import tkinter as tk
from logic import MinesweeperLogic

class MinesweeperGUI:
    def __init__(self, master, size, mines):
        self.master = master
        master.title("Minesweeper")
        self.logic = MinesweeperLogic(size, mines)  # Create an instance of the logic class

        # Calculate button size and window dimensions
        button_width = 30  # width of each button in pixels
        button_height = 30  # height of each button in pixels
        window_width = (size + 1) * button_width
        window_height = (size - 1) * button_height 

        # Initialize a grid of buttons
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        for row in range(size):
            for column in range(size):
                button = tk.Button(master, text='', width=3, height=1)
                button.grid(row=row, column=column)
                button.bind('<Button-1>', self.on_left_click(row, column))
                self.buttons[row][column] = button

        # Center the window
        self.center_window(window_width, window_height)

    def center_window(self, width, height):
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def on_left_click(self, row, column):
        """Handles left click for revealing the tile."""
        def callback(event):
            result = self.logic.reveal_cell(row, column)
            button = event.widget
            button.config(relief=tk.SUNKEN, state=tk.DISABLED)
        
        return callback
