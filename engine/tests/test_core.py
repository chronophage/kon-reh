import pytest
from konreh.core import Game

def test_game_boots():
    g = Game()
    assert g.turn == 1
    assert isinstance(g.legal_moves(), list)
