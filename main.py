import tkinter as tk

from display_gui import DisplayGui
from game import Game


if __name__ == "__main__":
    game = Game()
    root = tk.Tk()
    gui = DisplayGui(root, game)
    # gui.build_board()
    root.mainloop()
    # gui.run_game()
