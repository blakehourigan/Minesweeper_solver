import tkinter as tk


class EndSplashScreen: 
    def __init__(self, master, restart_game, destroy_game):
        self.master = master
        self.restart_game = restart_game
        self.exit_game = destroy_game
        self.master.title("Game Over")

        # Center the window
        self.master.geometry("300x100+{}+{}".format(
            master.winfo_screenwidth() // 2 - 150,
            master.winfo_screenheight() // 2 - 50
        ))

        # Make sure the game over window takes focus over the main application window
        self.master.grab_set()

        # Label displaying the game over message
        tk.Label(self.master, text="Game Over", font=("Helvetica", 16)).pack(pady=10)

        # Restart button
        tk.Button(self.master, text="Restart", command = self.restart_game).pack(side=tk.LEFT, padx=10)

        # Exit button
        tk.Button(self.master, text="Exit", command = self.exit_game).pack(side=tk.RIGHT, padx=10)

        # Disable the main window until the game over screen is closed
        master.wait_window(self.master)