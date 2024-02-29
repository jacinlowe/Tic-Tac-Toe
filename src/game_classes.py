from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell:
    character: str = None
    number: int = None

    def update_cell(self, cell: Cell):
        # check
        self.character = cell.character
        self.number = cell.number


Board = list[list[Cell]]
row = int
col = int
BOARD_INDEX = tuple[row, col]


class WinState(Enum):
    X_WIN = "X Wins"
    O_WIN = "O Wins"
    DRAW = "DRAW"
    CONTINUE = "CONTINUE"
