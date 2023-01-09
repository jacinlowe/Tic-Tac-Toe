from random import randint, choice
import time
from game_classes import Board, Cell


class CPU:
    def process_step(self, moves_list, turn):
        row = randint(0, 2)
        column = randint(0, 2)
        coords = (row, column)
        cell = Cell(character=turn, number=choice(moves_list))
        # time.sleep(2)
        return coords, cell
