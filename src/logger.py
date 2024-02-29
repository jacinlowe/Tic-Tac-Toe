"""
we need the
cell number
player
value chosen
"""

from dataclasses import dataclass


@dataclass
class LogItem:
    cell_num: int
    player: str
    value: int

    def __str__(self) -> str:
        return f"({self.cell_num}, {self.player}, {self.value})"


class Logger:
    def __init__(self) -> None:
        self.log_list = []

    def update_log(self, log: LogItem) -> None:
        self.log_list.append(log)

    def get_log(self) -> list[LogItem]:
        return self.log_list
