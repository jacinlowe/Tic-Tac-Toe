from __future__ import annotations


from .cpu import CPU
from .game_classes import BOARD_INDEX, Board, Cell, WinState
from .logger import LogItem, Logger

# from dataclasses import dataclass
# from enum import Enum
# from functools import partial
# import math


class Game:
    board: Board

    def __init__(self, isCpu: bool = False) -> None:
        self.board: list[list[Cell]] = None
        self.turn = "X"
        self.count = 0
        self.win_state = None
        self.isCpu = isCpu
        self.p1_move_list: list[int] = None
        self.p2_move_list: list[int] = None
        self.init_data()
        self.init_logger()

    def init_data(self):
        self.board = [[Cell() for i in range(3)] for c in range(3)]
        self.p1_move_list = [i for i in range(1, 8)]
        self.p2_move_list = [i for i in range(1, 8)]

    def init_logger(self):
        self.logger = Logger()

    def do_turn(self, index: int, cell: Cell):
        coords = get_row_col(index)
        # overwritable = partial(self.can_overwrite, coords, cell)
        if not self.can_overwrite(coords, cell):
            return False

        self.update_board(coords, cell)
        self.win_state = self.check_win_state()

        if self.turn == "X":
            self.decrease_move(cell.number, self.p1_move_list)
        else:
            self.decrease_move(cell.number, self.p2_move_list)

        self.increment_count()
        self.update_turn()
        update_logger(self.logger, index, cell)
        if self.isCpu:
            self.computer_step()
        return True

    def computer_step(self):
        # choose cell and value
        cpu = CPU()
        coords, cell = cpu.process_step(self.p2_move_list, self.turn)
        if not self.can_overwrite(coords, cell):
            self.computer_step()

        self.update_board(coords, cell)
        self.win_state = self.check_win_state()

        if self.turn == "X":
            self.decrease_move(cell.number, self.p1_move_list)
        else:
            self.decrease_move(cell.number, self.p2_move_list)

        update_logger(self.logger, coords_to_index(coords), cell)

        # self.increment_count()
        self.update_turn()

    def decrease_move(self, move_number: int, player: list[int]):
        print(f"player before decrease: {player}, {move_number}")
        player.remove(move_number)
        print(f"player after decrease: {player}")

    def can_overwrite(self, index: BOARD_INDEX, cell: Cell):
        row, col = index
        previous_cell = self.board[row][col]
        if previous_cell.number == None:
            return True
        elif cell.number > previous_cell.number:
            return True
        return False

    def increment_count(self):
        self.count += 1

    def update_turn(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"

    def check_win_state(self):
        current_board = self.board
        combined_move_list = self.p1_move_list + self.p2_move_list
        result = win_draw(current_board, combined_move_list)
        return result

    def update_board(self, coords, cell):
        row, col = coords
        self.board[row][col] = cell
        pass

    def get_board(self) -> Board:
        return self.board


def get_row(num: int):
    return num // 3


def get_col(num: int):
    return num % 3


def get_row_col(num: int) -> tuple[int, int]:
    return (get_row(num), get_col(num))


def coords_to_index(coords: tuple[int, int]) -> int:
    x, y = coords
    return y * 3 + x


def win_draw(board: Board, move_list: list):
    # 0 == draw
    # 2 == game still in play
    # 1 == O winner
    # -1 == X winner

    # checks win
    for i in range(3):
        # checks rows
        if board[i][0].character == board[i][1].character == board[i][2].character:
            if board[i][0].character != "":
                return (
                    WinState.O_WIN
                    if board[i][0].character == "O"
                    else WinState.X_WIN
                    if board[i][0].character == "X"
                    else WinState.CONTINUE
                )
        # checks columns
        if board[0][i].character == board[1][i].character == board[2][i].character:
            if board[0][i].character != "":
                return (
                    WinState.O_WIN
                    if board[0][i].character == "O"
                    else WinState.X_WIN
                    if board[0][i].character == "X"
                    else WinState.CONTINUE
                )
        # checks diagonals
        if (
            board[0][0].character == board[1][1].character == board[2][2].character
        ) or (board[2][0].character == board[1][1].character == board[0][2].character):
            if board[1][1].character != "":
                return (
                    WinState.O_WIN
                    if board[1][1].character == "O"
                    else WinState.X_WIN
                    if board[1][1].character == "X"
                    else WinState.CONTINUE
                )
    # checks draw
    # or if move list is empty
    return (
        WinState.DRAW
        if None not in [board[i][j].character for i in range(3) for j in range(3)]
        or len(move_list) == 0
        else WinState.CONTINUE
    )


def update_logger(logger: Logger, cell_index: int, cell: Cell):
    log = LogItem(cell_num=cell_index, player=cell.character, value=cell.number)
    logger.update_log(log)


if __name__ == "__main__":
    game = Game()
    cell = Cell("x", 7)
    print(game.can_overwrite(4, cell))
    # print()
