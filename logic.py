import random

from cell import Cell

class MinesweeperLogic:
    def __init__(self, grid_size, num_mines):
        # initializing logic variables
        self.num_mines = num_mines
        self.grid_size = grid_size
        self.board = [[Cell() for _ in range(grid_size)] for _ in range(grid_size)]
        self.num_moves = 0

    def reveal_cell(self, row, column):
        """Logic to reveal a cell; returns what's in the cell (mine, number, or empty)"""
        cell = self.board[row][column]
        if self.num_moves == 0:
            cell_type = 'empty'
            self.place_mines()
            self.fill_remaining_board()
            self.num_moves += 1
        else:
            cell_type = (cell).get_type()
            self.num_moves +=1
        return cell_type

    def toggle_flag(self, row, column):
        """ this function tells the gui to set a flag or unset flag based on user input and game state """
        cell = self.board[row][column]

        if (not cell.is_revealed) and not cell.get_type() == 'flag':
            cell.set_type("flag")
            return 'setflag'
        elif (not cell.is_revealed) and cell.get_type() == 'flag':
            cell.set_type("blank")
            return 'unset_flag'
        else:
            pass
        
    def place_mines(self):
        """ this function places mines on the board """
        total_mines = self.num_mines
        mines_placed = 0

        while mines_placed <= total_mines:
            row = random.randint(0, self.grid_size - 1)
            column = random.randint(0, self.grid_size - 1)

            # Check if the chosen cell already has a mine
            if not self.board[row][column].is_mine:
                self.board[row][column].set_type("mine")
                mines_placed += 1
    
    def fill_remaining_board(self):
        for row_number, row in enumerate(self.board):
            for col, cell in enumerate(row):
                if cell.get_type() == 'mine':
                    continue
                else:
                    cell.adjacent_mines = self.count_adjacents(row_number, col, cell)
                    cell.set_type(str(cell.adjacent_mines))

    def clear_adjacents(self):
        pass
    
    def count_adjacents(self, row, col, cell):
        """ function to count the number of adjacent bombs so we can calculate the numbers to place in other cells 
        count = 0
        # base cases
        if (row == 0 and col == 0) or (row == 0 and col == 8):
            if self.board[row][col].get_type == 'mine':
                count += 1 
            if self.board[row][col + 1].get_type == 'mine':
                count += 1 
            if self.board[row + 1][col].get_type == 'mine':
                count += 1 
        return count"""

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
        return True                    