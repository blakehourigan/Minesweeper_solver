import tkinter as tk
from logic import MinesweeperLogic

class MinesweeperGUI:
    def __init__(self, master, size, mines):
        self.master = master
        master.title("Minesweeper")
        self.logic = MinesweeperLogic(size, mines)  # Create an instance of the logic class

        # Initialize a 10x10 grid of buttons
        self.buttons = [[None for _ in range(size)] for _ in range(size)]
        for row in range(size):
            for column in range(size):
                button = tk.Button(master, text='', width=3, height=1)
                button.grid(row=row, column=column)
                button.bind('<Button-1>', self.on_left_click(row, column))
                self.buttons[row][column] = button

    def on_left_click(self, row, column):
        """Handles left click for revealing the tile."""
        def callback(event):
            result = self.logic.reveal_cell(row, column)  # Use the logic class to get the result of the click
            button = event.widget
            # Just change the button's relief to simulate a click for now
            button.config(relief=tk.SUNKEN, state=tk.DISABLED)
            # You would add game logic here to check for mines, etc.
        
        return callback

