# main.py
from tkinter import Tk
from welcome import WelcomeScreen

def main():
    root = Tk()
    app = WelcomeScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()
