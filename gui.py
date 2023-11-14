# gui.py
import tkinter as tk
import time

from logic import MinesweeperLogic
import config

class MinesweeperGUI:
    def __init__(self, master, size, mines, loss_window, win_window):
        self.master = master
        master.title("Minesweeper")
        self.loss_window = loss_window
        self.win_window = win_window
        self.logic = MinesweeperLogic(size, mines)  # Create an instance of the logic class
        
        self.mines_left = mines
        self.score = 0
        self.running = False
        
        self.setup_timer(self.master, size)
    
        self.load_image(self.master)

        self.setup_grid(self.master, size)

        # Initialize a grid of buttons with frames
        self.buttons = [[self.create_button(master, row + 1, column, config.button_width, config.button_height, size)
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
        # left click selects a cell
        button.bind('<Button-1>', lambda event, r=row, c=column: self.on_left_click(r, c)(event))
        # right click bound to setting flags
        button.bind('<Button-3>', lambda event, r=row, c=column: self.on_right_click(r, c)(event))

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
            # we need to adjust everything down by one, because an extra row is generated to house the timer and score labels
            logic_row, logic_column  = row - 1, column - 1 
            
            result = self.logic.reveal_cell(logic_row, logic_column)
            button = event.widget
            button.config(relief=tk.SUNKEN, state=tk.DISABLED)
            
            cell = self.logic.board[logic_row][logic_column]
            cell.is_revealed = True
            # check for a win
            if self.logic.check_for_win():
                self.win_window()
            # else, keep playing
            if result == 'empty':
                to_reveal = self.logic.clear_adjacents(logic_row, logic_column)
                self.clear_adjacents(to_reveal)
            elif result == 'mine':
                # Configure button image properties here
                button.config(image=self.mine_image, width=config.button_width, height=config.button_height)
                self.running = False
                self.reveal_board()
                time.sleep(5)  # Consider if this delay is necessary or optimal
                self.loss_window()
            elif str(result).isdigit() and result != '0':
                color = config.MINE_COLORMAP.get(result)
                button.config(text=result, bg=color, fg='white', width=config.button_width, height=config.button_height)
            else:
                pass
        return callback
    
    def reveal_board(self):
        """ function to reveal the whole board once you have lost the game """
        for row_index, row_entries in enumerate(self.logic.board):
            for col_index, cell in enumerate(row_entries):
                self._update_button_if_not_revealed(row_index, col_index, cell)

    def _update_button_if_not_revealed(self, row_index, col_index, cell):
        """ helper function to reveal a cell if it has not already been reveleaded before """
        if not cell.is_revealed:
            button = self.buttons[row_index][col_index]
            self._configure_button(button, cell)

    def _configure_button(self, button, cell):
        """ helper function to configure the button to color the cell based on cell type """
        cell_type = cell.get_type()
        color = config.MINE_COLORMAP.get(cell_type)
        button.config(relief=tk.SUNKEN, state=tk.DISABLED, bg=color)
        self.map_type_to_content(cell, button)
        self.master.update()
        
    def map_type_to_content(self, cell, button):
        if cell.type == 'mine':
            button.config(image=self.mine_image)
        elif cell.type != 'empty':
            button.config(text=cell.type)
        
    def clear_adjacents(self, to_reveal):
        for row, col in to_reveal:
            button = self.buttons[row][col]
            cell = self.logic.board[row][col]

            button.config(relief=tk.SUNKEN, state=tk.DISABLED)

            if cell.get_type() == 'empty':
                # Update button for an empty cell
                # You can configure it to have a different appearance if needed
                pass
            elif cell.get_type().isdigit():
                # Update button for a cell with adjacent mines
                color = config.MINE_COLORMAP.get(cell.get_type())
                button.config(text=cell.get_type(), bg=color, fg='white')
    
    def on_right_click(self, row, column):
        """Handles left click for revealing the tile."""
        def callback(event):
            button = event.widget
            if button.cget('relief') == tk.SUNKEN:
                return callback 
            else:
                action = self.logic.toggle_flag(row, column)
                if action == 'setflag':
                    button.config(image=self.flag_image, width=config.button_width, height=config.button_height )
                elif action == 'unset_flag':
                    button.config(relief=tk.RAISED)
                    button.config(image=self.flag_image, width=config.button_width, height=config.button_height)
                    button.config(image='')
                else:
                    pass
        return callback

    def load_image(self, master):
        # Get the appropriate icon file based on the OS
        icon_file = config.get_task_tray_icon()

        if icon_file.endswith('.ico'):
            master.iconbitmap(icon_file)
        else:
            tt_img = tk.PhotoImage(file=icon_file)
            master.iconphoto(True, tt_img)

        # Load the mine image once and keep a reference
        self.mine_image = tk.PhotoImage(file=config.mine_image)
        self.flag_image = tk.PhotoImage(file=config.flag_image)

    def setup_grid(self, master, size):
        # Adjust layout for the new elements
        master.grid_rowconfigure(1, weight=1)  # Adjusting for the new row with labels
        # create layout for the elements on the screen
        master.grid_rowconfigure(0, weight=0)  
        for i in range(1, size + 1):
            master.grid_rowconfigure(i, weight=1)  # Create a grid that has height of size + 1 to fit timer and score labels
        for i in range(size):
            master.grid_columnconfigure(i, weight=1)

    def setup_timer(self, master, size):
        """ function to setup the timer labels and set the timer to running """
        self.timer_label = tk.Label(master, text="Time: 0s")
        self.timer_label.grid(row=0, column=0, columnspan=size//2, sticky="w")

        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.grid(row=0, column=size//2, columnspan=size//2, sticky="e")
        if not self.running:
            self.start_time = time.time()
            self.running = True
            self.update_timer()

    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_timer)