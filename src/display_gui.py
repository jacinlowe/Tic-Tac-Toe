from functools import partial
import tkinter as tk
from tkinter import messagebox
from typing import Literal


from .button import ButtonPanel
from .game import Cell, Game
from .game_classes import WinState

FONT, FONT2, FONT3 = ("Arial", 70), ("Arial", 20), ("Arial", 16)


class DisplayGui(tk.Frame):
    def __init__(self, parent: tk.Tk, game: Game, config: int = 0):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.game = game
        self.button_list: list[tk.Button] = []
        self.move_list = (
            self.game.p1_move_list if self.game.turn == "X" else self.game.p2_move_list
        )
        self.move_list_toggle_states = ["raised" for i in self.move_list]
        self.move_buttons: ButtonPanel = None
        self.current_number = None
        self.radio = tk.StringVar()
        self.radio.set(config)
        self.initialize_ui()

    def initialize_ui(self):
        self.parent.title("7 Tac Toe")
        self.pack(fill=tk.BOTH, expand=1)
        self._initialize_menu()
        self._initialize_grid()
        self._initialize_counters()

    def change_player(self, choice: tk.StringVar):
        value = choice.get()
        print(value)

        if value == "0":
            self.new_game()
        if value == "1":
            self.new_game()
        if value == "2":
            self.new_game()

    def _initialize_menu(self):
        gamemode_va = tk.IntVar()
        gamemode_va.set(0)
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            # label="Reset Game", command=partial(new_game, self.parent)
            label="Reset Game",
            command=self.new_game,
        )

        gamemode_menu = tk.Menu(file_menu, tearoff=False)

        gamemode_menu.add_radiobutton(
            label="VS CPU",
            value=0,
            variable=self.radio,
            state=tk.ACTIVE,
            command=(lambda: self.change_player(self.radio)),
        )
        gamemode_menu.add_radiobutton(
            label="VS Smart CPU",
            value=1,
            variable=self.radio,
            command=(lambda: self.change_player(self.radio)),
        )
        gamemode_menu.add_radiobutton(
            label="VS Player",
            value=2,
            variable=self.radio,
            command=(lambda: self.change_player(self.radio)),
        )
        file_menu.add_cascade(label="Game Modes", menu=gamemode_menu)
        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=self.destroy)
        self.parent.config(menu=menubar)
        menubar.add_cascade(label="File", menu=file_menu)

    def test_cmd(self):
        pass

    def _initialize_grid(self):
        grid_frame = tk.Frame(self)
        for i in range(3):
            for j in range(3):
                index = (i + 1) * (j + 1)
                button = tk.Button(
                    grid_frame,
                    text="",
                    font=("Helvetica", "20"),
                    width=4,
                    height=2,
                    command=partial(callback, (i, j), self.do_turn),
                )
                button.grid(row=i, column=j)
                self.button_list.append(button)
        grid_frame.pack()

    def intialize_move_list(self):
        self.move_buttons = ButtonPanel(self)
        self.move_buttons.init_btns(self.game.p1_move_list)

    def set_current_number(self, num: int):
        self.current_number = num

    def reset_current_number(self):
        self.current_number = None

    def _initialize_counters(self):
        frame2 = tk.Frame(self)
        self.turn_label = tk.Label(frame2, text=f"Turn {self.game.turn}", font=FONT2)
        self.turn_count = tk.Label(frame2, text=f"Moves: {self.game.count}", font=FONT2)
        self.status_label = tk.Label(frame2, text=f"{self.game.win_state}", font=FONT2)
        self.moves_left = tk.Label(frame2, text=f"{self.move_buttons}", font=FONT2)

        self.intialize_move_list()
        self.status_label.grid(row=0)
        # self.moves_left.grid(row=1)
        self.turn_label.grid(row=2)
        self.turn_count.grid(row=3)

        frame2.pack()

    def update_counters(self):
        self.turn_count.config(text=f"Moves: {self.game.count}")
        self.turn_label.config(text=f"Turn {self.game.turn}")
        # self.intialize_move_list()
        self.update_status()

    def update_status(self, message: str = None):
        if message == None:
            self.status_label.config(text=f"{self.game.win_state.value}")
        else:
            self.status_label.config(text=message)

    def update_board(self):
        board = self.game.get_board()
        for i in range(3):
            for j in range(3):
                index = get_index((i, j))
                cell = board[i][j]
                self.update_cell(index, cell)

    def update_cell(self, index, cell: Cell):
        if cell.character == None or cell.number == None:
            return
        self.button_list[index].configure(text=f"{cell.character} {cell.number}")
        cell_text = self.button_list[index].cget("text")
        print(cell_text)

    def update_move_list_display(self):
        # self.move_buttons.frame.pack_forget()
        # self.move_buttons.init_btns(self.game.p1_move_list)
        if self.game.turn == "X":
            self.move_buttons.update_button_frame(self.game.p1_move_list)
        else:
            self.move_buttons.update_button_frame(self.game.p2_move_list)

    def do_turn(self, coords: tuple[int, int]):
        self.unbind_board()
        index = get_index(coords)
        # if self.current_number == None:
        #     return
        btn_num = self.move_buttons.active_btn

        if btn_num == None:
            self.update_status("Please select a value then select a grid position!")
            self.bind_board()
            return

        cell = Cell(self.game.turn, int(btn_num))
        can_update = self.game.do_turn(index, cell)
        if not can_update:
            self.update_status("Cannot Overwrite position, Try another cell!")
            self.bind_board()
            return
        self.update_board()
        self.update_counters()
        # self.move_buttons.remove_btn()
        self.reset_current_number()
        if self.game.win_state != WinState.CONTINUE:
            # Display a graphic or show player in big letters that they won or lost
            return
        self.update_move_list_display()
        for i in self.game.logger.get_log():
            print(i)
        self.bind_board()

    def unbind_board(self):
        for btn in self.button_list:
            btn["state"] = "disabled"

    def bind_board(self):
        for btn in self.button_list:
            btn["state"] = "normal"

    def new_game(self):
        root = self.parent
        gamestate = self.radio.get()
        isCpu = True if gamestate == "0" or gamestate == "1" else False
        self.destroy()
        game = Game(isCpu=isCpu)
        gui = DisplayGui(root, game, int(gamestate))


def callback(arg1, arg2: callable):
    arg2(arg1)
    # print(f"Button was clicked with arguments {arg1} and {arg2}")


def get_index(coords, num_cols=3):
    x, y = coords
    return x * num_cols + y


def print_callback(arg1) -> None:
    print(arg1)


def quit(root):
    ask_exit = messagebox.askyesno(
        title="Quit", message="Are you sure you want to quit?"
    )
    if ask_exit > 0:
        root.destroy()
        return


def new_game(parent: tk.Frame):
    print("new game")
    parent.destroy()
    game = Game()
    root = tk.Tk()
    gui = DisplayGui(root, game)
    # gui.build_board()
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    ttt = DisplayGui(root)
    root.mainloop()
