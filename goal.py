"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    lst = []
    randomint = random.randint(0, 1)
    colours = COLOUR_LIST.copy()
    if randomint == 0:
        for _ in range(num_goals):
            random.shuffle(colours)
            colour = colours.pop()
            goal = PerimeterGoal(colour)
            lst.append(goal)

    if randomint == 1:
        for _ in range(num_goals):
            random.shuffle(colours)
            colour = colours.pop()
            goal = BlobGoal(colour)
            lst.append(goal)
    return lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    lim = 2 ** (block.max_depth - block.level)
    i = 0

    if len(block.children) == 0:
        val = [[block.colour] * lim]
        return val * lim
    else:
        first, second = [], []
        flattened_ch0 = _flatten(block.children[0])
        flattened_ch1 = _flatten(block.children[1])
        flattened_ch2 = _flatten(block.children[2])
        flattened_ch3 = _flatten(block.children[3])

        while i < len(flattened_ch0):
            first.extend([flattened_ch1[i] + flattened_ch2[i]])
            second.extend([flattened_ch0[i] + flattened_ch3[i]])
            i += 1

        return first + second


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """
    Perimeter goal is the aim to put the most possible units of a given colour
    c on the outer perimeter of the board. Calculated score is the total number
    of unit cells of colour c that are on the perimeter. There is a premium on
     corner cells: they count twice towards the score.

    === Attributes ===
        colour:
            The target colour for this goal, that is the colour to which
            this goal applies.
    """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """return the score for player with goal PerimeterGoal using <board>"""
        fattened_board = _flatten(board)
        colour = self.colour
        score = 0
        i = 0

        while i < len(fattened_board):
            if fattened_board[0][i] == colour:
                score += 1
            if fattened_board[i][0] == colour:
                score += 1
            if fattened_board[i][-1] == colour:
                score += 1
            if fattened_board[-1][i] == colour:
                score += 1
            i += 1
        return score

    def description(self) -> str:
        """Return a description of this Perimeter goal.
        """
        return "Make the largest connected \' perimeter \' of " \
               + colour_name(self.colour)


class BlobGoal(Goal):
    """
    The player must aim for the largest “blob” of a given colour c.
       A blob is a group of connected blocks with the same colour. Two blocks
       are connected if their sides touch; touching corners doesn’t count. The
       player’s score is the number of unit cells in the largest blob of
       colour c.
    === Attributes ===
   colour:
       The target colour for this goal, that is the colour to which
       this goal applies.
    """
    colour: Tuple[int, int, int]

    def score(self, board: Block) -> int:
        """return the score for player with goal BlobGoal using <board>"""
        flattened_board = _flatten(board)
        score = 0
        board_len = len(flattened_board)
        visited = []

        for row in range(board_len):
            column = []
            for col in range(len(flattened_board[row])):
                column.append(-1)
            visited.append(column)

        for row in range(len(flattened_board)):
            for col in range(len(flattened_board[row])):
                cell = (row, col)
                contender = self._undiscovered_blob_size(cell,
                                                         flattened_board,
                                                         visited)
                if contender > score:
                    score = contender
                else:
                    pass
        return score

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        row = pos[0]
        col = pos[1]
        if col < 0 or col >= len(board) or row < 0 or row >= len(board) or\
                visited[col][row] != -1:
            return 0

        elif self.colour != board[col][row]:
            visited[col][row] = 0
            return 0
        else:

            visited[col][row] = 1
            positions = [(row, col + 1), (row, col - 1), (row + 1, col),
                         (row - 1, col)]
            total = 1
            for location in positions:
                total += self._undiscovered_blob_size(location, board, visited)
            return total

    def description(self) -> str:
        """Return a description of this goal.
        """
        return "Make the largest connected \' blob \' of " \
               + colour_name(self.colour)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
