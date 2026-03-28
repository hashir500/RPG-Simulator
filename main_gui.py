import tkinter as tk
from game_view import GameApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("RPG Battle Simulator")
    root.geometry("800x600")
    root.resizable(False, False)
    app = GameApp(root)
    root.mainloop()