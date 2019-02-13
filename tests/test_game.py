import pytest
import context # setups sys.path

from game import lib
from game.lib import model
from game.lib import space_cube


def test_matrix():
    matrix = lib.create_3d_matrix(2,3,4)
    assert matrix[1][2][3] is None
    with pytest.raises(IndexError):
        matrix[2][2][3]
    with pytest.raises(IndexError):
        matrix[1][3][3]
    with pytest.raises(IndexError):
        matrix[1][2][4]


def test_spacecube():
    pass
