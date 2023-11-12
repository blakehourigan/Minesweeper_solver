# game_manager.py
import tkinter as tk
from gui import MinesweeperGUI
import config

class GameManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        # Get the appropriate icon file based on the OS
        icon_file = config.get_task_tray_icon()
        if icon_file.endswith('.ico'):
            self.root.iconbitmap(icon_file)
        else:
            tt_img = tk.PhotoImage(file=icon_file)
            self.root.iconphoto(True, tt_img)

    def start_welcome_screen(self, welcome_class):
        # welcome class is passed into this function, we initialize the class to start the welcome screen, and pass in the callback funciton to begine the game
        welcome_screen = welcome_class(self.root, self.start_game)
        self.root.mainloop()

    def start_game(self, difficulty):
        settings = config.DIFFICULTIES.get(difficulty, config.DIFFICULTIES["Beginner"])
        # destroy the welcome window and create the game window
        self.root.destroy()
        game_root = tk.Tk()
        MinesweeperGUI(game_root, **settings)
        game_root.mainloop()
