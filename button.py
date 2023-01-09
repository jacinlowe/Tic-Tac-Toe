from functools import partial
import tkinter as tk


class Button:
    def __init__(self, root, value: str):
        self.value: str = value
        self.var = tk.StringVar()

        self.selected = tk.BooleanVar()
        self.button = tk.Button(
            root,
            text=value,
            command=self.get_value,
            font=("Helvetica", "10"),
            width=2,
            height=1,
        )
        self.var.set(value)
        # self.button.pack()

    def set_value(self):
        self.var.set(self.value)

    def get_value(self):
        value = self.var.get()
        # self.selected.set(True)
        # self.var.trace_add("write", self.callback)
        # print(f"Button with value '{value}' was toggled")
        return value

    def callback(self, *args):
        value = self.var.get()
        # print(f"button value was changed {value}")


class ButtonPanel:
    def __init__(
        self,
        parent,
    ) -> None:
        self.rootFrame = tk.Frame(parent)
        self.frame = tk.Frame(self.rootFrame)
        self.active_btn: str = None
        self.rootFrame.pack()
        self.button_list: list[Button] = []

    def init_btns(self, player_moves: list[int]):
        print(player_moves)
        for i, player_move in enumerate(player_moves):
            # print(i, player_move)
            button = Button(self.frame, str(player_move))
            button.button.grid(row=1, column=i)
            btn = button.button
            btn.configure(command=partial(self.callback_commands, player_move))
            self.button_list.append(button)
        self.frame.pack()

    def callback_commands(self, btn_num: int):

        index = get_btn_index(self.button_list, str(btn_num))
        btn = self.button_list[index]
        self.active_btn = btn.get_value()
        self.toggle_btn(index)
        # print(f"Active Btn: {self.active_btn}")

    def toggle_btn(self, index: int):
        # print(index)
        for i, btn in enumerate(self.button_list):
            if index == i:
                btn.button.configure(relief="sunken")
            else:
                btn.button.configure(relief="raised")

    def remove_btn(self):
        index = get_btn_index(self.button_list, self.active_btn)
        btn = self.button_list[index]

        btn.button.destroy()
        self.button_list.remove(self.button_list[index])
        self.active_btn = None
        # print(f"button was destroyed{btn.get_value()}")

    def update_button_frame(self, player_moves: list[int]):
        self.button_list = []
        # self.frame.pack_forget()
        self.frame.destroy()
        self.frame = tk.Frame(self.rootFrame)
        for i, player_move in enumerate(player_moves):
            button = Button(self.frame, str(player_move))
            button.button.grid(row=1, column=i)
            btn = button.button
            btn.configure(command=partial(self.callback_commands, player_move))
            print(f"button created: {button.value}")
            self.button_list.append(button)
        print(len(self.button_list))
        self.frame.pack()


def get_btn_index(btn_list: list[Button], btn_num) -> int:
    for index, btn in enumerate(btn_list):
        if btn.value == btn_num:
            # print(f"button index: {index}")
            return index


"""
In this example, the MyButton class defines a button with a value attribute and a StringVar instance variable. The set_value method sets the value of the StringVar to the value attribute of the button.

To get the value of the toggled button, the callback function iterates over the list of buttons and checks the relief option of each button using the

"""
