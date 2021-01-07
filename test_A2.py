from __future__ import annotations
from typing import Optional, Tuple, List
import random
import math
from block import Block, generate_board
from settings import colour_name, COLOUR_LIST
from goal import generate_goals, Goal
import pytest

def test_str__()-> None:
    block = Block((0, 0), 750, (1, 128, 181), 0, 1)
    assert str(block) == 'Leaf: colour=Pacific Point, pos=(0, 0), size=750, ' \
                         'level=0\n'
def test_update_children_positions()-> None:
    block = Block((0, 0), 750, (1, 128, 181), 0, 1)
    top_right_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    top_left_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    bottom_left_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    bottom_right_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    block.children = [top_right_child, top_left_child, bottom_left_child, bottom_right_child]
    block._update_children_positions((1, 1))
    assert str(block) == ''

def test_smashable() -> None:
    block = Block((0, 0), 750, (1, 128, 181), 0, 3)
    top_right_child = Block((0, 0), 750, (1, 128, 181), 1, 3)
    top_left_child = Block((0, 0), 750, (1, 128, 181), 1, 1)
    bottom_left_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    bottom_right_child = Block((0, 0), 750, (1, 128, 181), 0, 1)
    block.children = [top_right_child, top_left_child, bottom_left_child,
                      bottom_right_child]
    assert block.smashable() == False
    assert top_right_child.smashable() == True
    assert top_left_child.smashable() == False


##Test smash and its helper function
##test swap, rotate and all other functions from block and blocky
##test generate_goals, and to see if no two goals have same colour
##complete _flatten and test it
##check wether we need to implement an initializer in the subclass of Goal class
##test the _get_block and create_players in player.py
##for create players i need to make sure that the
##do we need to make copies for swap and rotate
### we copied   rotate and _get_block
##when decreasing / increasing level in game, the level sometiems
### _flatten change variables and maybe the structure of the code copied from github
###copied score from github, change atrribute names and code
##copied score and _udiscovered_blob_size. Change attribute names and code
###check how to create_copy of the block
##update the attributes docstrings of SmartPlayer and RandomPlayer class
###ADD COMBINE FROM
