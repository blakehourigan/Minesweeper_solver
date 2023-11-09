import tkinter as tk
from gui import MinesweeperGUI

class WelcomeScreen:
    def __init__(self, master):
        self.master = master
        master.title("Welcome to Minesweeper")

        tk.Label(master, text="Welcome to Minesweeper! Choose your difficulty:").pack()

        self.difficulty = tk.StringVar(master)
        self.difficulty.set("Beginner")  # default value

        options = ["Beginner", "Intermediate", "Expert"]
        tk.OptionMenu(master, self.difficulty, *options).pack()

        tk.Button(master, text="Start Game", command=self.start_game).pack()

    def start_game(self):
        difficulty = self.difficulty.get()
        # Translate difficulty to game settings (size and mine count)
        if difficulty == "Beginner":
            size, mines = 9, 10
        elif difficulty == "Intermediate":
            size, mines = 16, 40
        elif difficulty == "Expert":
            size, mines = 24, 99
        else:
            size, mines = 9, 10  # Fallback to default

        self.master.destroy()  # Close the welcome screen
        game_root = tk.Tk()  # Create a new Tk root for the game
        game = MinesweeperGUI(game_root, size, mines)  # Start the game with the chosen difficulty
        game_root.mainloop()