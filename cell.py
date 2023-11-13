class Cell:
    def __init__(self):
        self.type = "empty"
        self.is_mine = False
        self.adjacent_mines = 0
        self.is_revealed = False

    def __str__(self):
        return f"Type: {self.type} \n# Adjacent mines: {self.adjacent_mines}\nRevealed: {self.is_revealed}"
    
    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type
        
