import tkinter as tk

from logic import MinesweeperLogic
import config

class MinesweeperGUI:
    def __init__(self, master, size, mines):
        self.master = master
        master.title("Minesweeper")
        self.logic = MinesweeperLogic(size, mines, size)  # Create an instance of the logic class

        # Load the mine image once and keep a reference
        self.mine_image = tk.PhotoImage(file=config.mine_image)

        # Set the master frame's row and column configurations
        for i in range(size):
            master.grid_columnconfigure(i, weight=1)
            master.grid_rowconfigure(i, weight=1)

        # Initialize a grid of buttons with frames
        self.buttons = [[self.create_button(master, row, column, config.button_width, config.button_height, size)
                        for column in range(size)] for row in range(size)]

        # Disable window resizing
        master.resizable(False, False)

        # Set the minimum window size to accommodate the grid
        window_width = size * config.button_width
        window_height = size * config.button_height
        master.minsize(window_width, window_height)

        # Center the window
        self.center_window(window_width, window_height)

    def create_button(self, master, row, column, width, height, size):
        # Create a frame to hold the button
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")  # Use sticky to fill the space
        


        # Create the button and pack it into the frame
        button = tk.Button(frame, width=config.button_width,height=config.button_height)
        button.bind('<Button-1>', lambda event, r=row, c=column: self.on_left_click(r, c)(event))
        button.pack(expand=True, fill='both')  # Button will fill the entire frame

        return button

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

            if result == 'mine':
                # Configure button image properties here
                button.config(image=self.mine_image, width=config.button_width, height=config.button_height)
            else:
                pass
        return callback

