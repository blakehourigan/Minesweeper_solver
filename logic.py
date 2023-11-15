# logic.py
import random

from cell import Cell

class MinesweeperLogic:
    def __init__(self, grid_size, num_mines):
        # initializing logic variables
        self.num_mines = num_mines
        self.grid_size = grid_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.num_moves = 0
        self.score = 0
        self.running = False

    def print_board(self):
        print("Minesweeper Board:")
        for row in self.board:
            row_str = ''
            for cell in row:
                celltype = (cell).get_type()
                if celltype == 'mine':
                    row_str += 'M '  # Mine
                elif cell.adjacent_mines > 0:
                    row_str += f'{cell.adjacent_mines} '  # Number of adjacent mines
                else:
                    row_str += 'E '  # Empty cell
            print(row_str)
        print()  # Newline for readability

    def initialize_mines(self):
        self.place_mines()
        self.fill_remaining_board()

    def print_board(self):
        print("Minesweeper Board:")
        for row in self.board:
            row_str = ''
            for cell in row:
                celltype = (cell).get_type()
                if celltype == 'mine':
                    row_str += 'M '  # Mine
                elif cell.adjacent_mines > 0:
                    row_str += f'{cell.adjacent_mines} '  # Number of adjacent mines
                else:
                    row_str += 'E '  # Empty cell
            print(row_str)
        print()  # Newline for readability

    def initialize_mines(self):
        self.place_mines()
        self.fill_remaining_board()
    
    def reveal_cell(self, row, column):
        """Logic to reveal a cell; returns what's in the cell (mine, number, or empty)"""
        cell = self.board[row][column]
        if self.num_moves == 0:
            cell.set_type('empty')
            self.place_mines()
            self.fill_remaining_board()
            self.score += 1
            self.num_moves += 1
        if cell.get_type != 'mine' and self.num_moves > 0:
            self.score += 1
            self.num_moves +=1
        return cell.get_type()

    def toggle_flag(self, row, column):
        """ this function tells the gui to set a flag or unset flag based on user input and game state """
        cell = self.board[row][column]

        if (not cell.is_revealed) and not cell.is_flagged:
            cell.is_flagged = True
            return 'setflag'
        elif (not cell.is_revealed) and cell.is_flagged:
            cell.is_flagged = False
            return 'unset_flag'
        else:
            print('Unexpected error, please reload program and play again')
            exit(1)
        
    def place_mines(self):
        """ this function places mines on the board """
        total_mines = self.num_mines
        mines_placed = 0

        while mines_placed <= total_mines:
            row = random.randint(0, self.grid_size - 1)
            column = random.randint(0, self.grid_size - 1)

            cell = self.board[row][column]
            
            # Place mines in any cell other than the inital one
            if cell.get_type() == 'blank':
                cell.set_type("mine")
                cell.is_mine = True
                mines_placed += 1
    
    def fill_remaining_board(self):
        """ after bombs are placed, we fill the rest of the cells with numbers or empty spaces"""
        for row_number, row in enumerate(self.board):
            for col, cell in enumerate(row):
                if cell.get_type() == 'mine':
                    continue
                elif self.count_adjacents(row_number, col) > 0 and cell.get_type() == 'blank':
                    cell.adjacent_mines = self.count_adjacents(row_number, col)
                    cell.set_type(str(cell.adjacent_mines))
                else:
                    cell.set_type("empty")

    def clear_adjacents(self, row, col): 
        """ function that checks if adjacent cells are empty, and if so it clears them"""
        to_reveal = set()       # this set is used keep track of if cells are found that need to be revealed locally
        to_reveal.add((row, col))

        revealed_cells = set()  # Set to keep track of all the cells that need to be revealed globally on all iterations 

        while to_reveal:
            current_row, current_col = to_reveal.pop()
            curr_cell = self.board[current_row][current_col]

            # If the cell is already revealed or is a mine, skip it
            if (current_row, current_col) in revealed_cells or self.board[current_row][current_col].get_type() == 'mine':
                continue

            revealed_cells.add((current_row, current_col))
            curr_cell.is_revealed = True

            # If the current cell is empty, add its neighbors to the set
            if curr_cell.get_type() == 'empty':
                neighbor_positions = [(-1, -1), (-1, 0), (-1, 1),  # adjacent above row
                                    (0, -1),           (0, 1),    # adjacent same row
                                    (1, -1), (1, 0), (1, 1)]     # adjacent below row

                for row_offset, col_offset in neighbor_positions:
                    neighbor_row, neighbor_col = current_row + row_offset, current_col + col_offset
                    # Check if the neighbor is within the bounds of the board
                    if 0 <= neighbor_row < len(self.board) and 0 <= neighbor_col < len(self.board[0]):
                        neighbor_cell = self.board[neighbor_row][neighbor_col]
                        # Add the cell to be revealed if it is not a mine and not already revealed
                        if not neighbor_cell.is_mine and not neighbor_cell.is_revealed:
                            to_reveal.add((neighbor_row, neighbor_col))
        self.score += len(revealed_cells)
        return revealed_cells

    def count_adjacents(self, row, col):
        """ function that checks the adjacent cells for mines if they exist """
        neighbor_positions = [(-1, -1), (-1, 0), (-1, 1),  # Above row
                            (0, -1),           (0, 1),    # Same row
                            (1, -1), (1, 0), (1, 1)]     # Below row

        count = 0
        for row_offset, col_offset in neighbor_positions:
            neighbor_row, neighbor_col = row + row_offset, col + col_offset
            # Check if the neighbor is within the bounds of the board
            if 0 <= neighbor_row < len(self.board) and 0 <= neighbor_col < len(self.board[0]):
                if self.board[neighbor_row][neighbor_col].get_type() == 'mine':
                    count += 1

        return count

    def check_for_win(self):
        """function to check if the player has won the game"""
        for row in self.board:
            for cell in row:
                # if we find a cell that is not a mine and is not revealed yet, then we need to keep going
                if not cell.type == 'mine' and not cell.is_revealed:
                    return False
        self.score += (self.num_mines * 15) 
        return True                    
    
    def get_score(self):
        return self.score