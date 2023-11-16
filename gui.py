# gui.py
import tkinter as tk
import time
import threading
import openpyxl

import config

class MinesweeperGUI:
    def __init__(self, master, size, mines, player, loss_window, win_window, logic, AI, ai_solution=None):
        self.master = master
        if not ai_solution:
            master.title("Minesweeper")
        self.loss_window = loss_window
        self.win_window = win_window
        self.ai_solution = ai_solution
        self.logic = logic
        self.AI = AI
        self.size = size 
        self.player = player
        self.mines = mines

        self.setup_timer(self.master, size)
    
        self.load_image(self.master)

        self.setup_grid(self.master, size)
        
        self.flag_images = {}  # Dictionary to store flag images for AI winows
        
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
        if player == "AI" and ai_solution is None:  # This prevents the infinite loop
            self.logic.initialize_board_AI()
            self.reveal_board()
            ga_thread = threading.Thread(target=self.run_genetic_algorithm)
            ga_thread.start()
        elif ai_solution is not None:
            self.reveal_board()
            self.overlay_ai_flags(ai_solution)  # Call this method to display the AI's flags


    def run_genetic_algorithm(self):
        start_time = time.time()
        final_solutions = self.AI.run_multiple_ga_iterations(
            config.ITERATIONS, config.POPULATION_SIZE, config.GENERATIONS, 
            config.TOURNAMENT_SIZE, config.MUTATION_RATE, config.CROSSOVER_RATE, 
            self.logic.num_mines, config.ELITISM_COUNT)
        end_time = time.time()
        self.AI_exec_time = end_time - start_time
        for i, solution in enumerate(final_solutions):
            self.master.after(0, self.show_ai_solution, i, solution)       

        # Create a new Excel workbook and select the active sheet
        wb = openpyxl.Workbook()
        sheet = wb.active

        # Set headers
        headers = ["Execution Time", "Solution Number", "Flags", "Mines", "Missing Mines", "Fitness", "# Flags in solution", "Total mines", "# Correct Flags", "% Correctly Identified","Max Possible Fitness"]
        sheet.append(headers)
        sheet['A2'] = str(self.AI_exec_time)
        for i, solution in enumerate(final_solutions):
            # Assuming 'root' is your Tkinter root window and 'ai_solution' is an instance of 'Individual' with the AI's flags
            solution_number = f"Solution {i+1}"
            flags_str = str(solution.flags)
            mine_coords_str = str(self.logic.mine_coords)
            missing_mines = ', '.join(str(s) for s in (self.logic.mine_coords - solution.flags) if s)            
            fitness_str = str(solution.fitness)
            flag_num_str = str(len(solution.flags))
            correct_flags = str(self.logic.num_mines - len(self.logic.mine_coords - solution.flags))
            pct_correct = ((self.logic.num_mines - len(self.logic.mine_coords - solution.flags)) / self.logic.num_mines) * 100 

            mines_str = str(self.logic.num_mines)

            # Append the data to the sheet
            sheet.append(["",solution_number, flags_str, mine_coords_str, missing_mines, fitness_str, flag_num_str, mines_str, correct_flags, pct_correct,self.AI.maximum_fitness()])
        # Save the workbook to a file
        wb.save("genetic_algorithm_results.xlsx")
        print("Data Written...")


    def show_ai_solution(self, solution_index,ai_solution):
        """Creates a new window to display the AI's flags."""
        # Create a Toplevel window
        top = tk.Toplevel(self.master)
        top.title(f"AI's Solution #{solution_index + 1}")
                
        # Create an instance of MinesweeperGUI inside the new window
        # Pass the ai_solution to the new GUI
        ai_gui = MinesweeperGUI(top, self.logic.grid_size, self.logic.num_mines, "AI", 
                                self.loss_window, self.win_window, self.logic, self.AI, 
                                ai_solution=ai_solution)

    def overlay_ai_flags(self, ai_solution):
        """Overlays AI's flags on the board."""
        for row in range(self.logic.grid_size):
            for col in range(self.logic.grid_size):
                button = self.buttons[row][col]
                # If the current cell is flagged by the AI, overlay the flag image
                if (row, col) in ai_solution.flags:
                    if (row, col) not in self.flag_images:
                        self.flag_images[(row, col)] = tk.PhotoImage(file=config.flag_image)
                    button.config(relief=tk.RAISED, image=self.flag_images[(row, col)])
                    button.image = self.flag_images[(row, col)]  # Keep a reference

    def create_button(self, master, row, column, width, height, size):
        # Create a frame to hold the button
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")  # Use sticky to fill the space
        
        # Create the button
        button = tk.Button(frame, width=config.button_width,height=config.button_height)
        
        if self.player != 'AI':
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
            logic_row, logic_column  = row - 1, column 
            
            result = self.logic.reveal_cell(logic_row, logic_column)
            button = event.widget

            cell = self.logic.board[logic_row][logic_column]

            self._configure_button(button, cell)
            # check for a win
            if self.logic.check_for_win():
                self.win_window()
            # else, keep playing
            if result == 'empty':
                to_reveal = self.logic.clear_adjacents(logic_row, logic_column)
                self.clear_adjacents(to_reveal)
            elif result == 'mine':
                self.logic.running = False
                # reveal the board to the player for 5s
                self.reveal_board()

                time.sleep(5) 
                self.loss_window()
            elif cell.is_numbered():
                self._configure_button(button, cell)
            else:
                print("Error: cell type not allowed")
                exit(1)
            self.update_score()
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

    def _configure_button(self, button, cell, action = None):
        """ helper function to configure the button to color the cell based on cell type """
        if action:
            if action == 'setflag':
                button.config(image=self.images['flag'], width=config.button_width, height=config.button_height )
            elif action == 'unset_flag':
                button.config(relief=tk.RAISED)
                button.config(image=self.images['flag'], width=config.button_width, height=config.button_height)
                button.config(image='')
        else:
            cell_type = cell.get_type()
            color = config.MINE_COLORMAP.get(cell_type)
            button.config(relief=tk.SUNKEN, state=tk.DISABLED, bg=color)
            if cell.type == 'mine':
                button.config(relief=tk.RAISED, state=tk.DISABLED, bg=color)
                button.config(image=self.images['mine'])
            elif cell.type != 'empty' and cell.type != 'flag':
                button.config(text=cell.type)
        self.master.update()

    def clear_adjacents(self, to_reveal):
        """ this function clears the adjacent cells if the cell the user clicks is empty """
        for row, col in to_reveal:
            button = self.buttons[row][col]
            cell = self.logic.board[row][col]
            self._configure_button(button, cell)
    
    def on_right_click(self, row, column):
        """Handles left click for revealing the tile."""
        def callback(event):
            logic_row, logic_column  = row - 1, column
            
            button = event.widget
            cell = self.logic.board[logic_row][logic_column]
            if button.cget('relief') == tk.SUNKEN:
                return callback 
            else:
                action = self.logic.toggle_flag(logic_row, logic_column)
                self._configure_button(button, cell, action)

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
        self.images = {
            'mine': tk.PhotoImage(file=config.mine_image),
            'flag': tk.PhotoImage(file=config.flag_image)
        }

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
        if not self.logic.running:
            self.start_time = time.time()
            self.logic.running = True
            self.update_timer()

    def update_timer(self):
        if self.logic.running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_timer)
    
    def update_score(self):
        if self.logic.running:
            self.score_label.config(text=f"Score: {self.logic.get_score()}")