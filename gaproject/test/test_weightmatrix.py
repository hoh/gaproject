'''
Tests for the MetaGA WeightMatrix
'''

import pytest

from gaproject.metaga import WeightMatrix


def test_dict_operations():
    m = WeightMatrix()

    couple = (2, 3)
    value = 2

    m[couple] = value
    assert couple in m
    assert m[couple] == value
    del m[couple]


def test_add():
    m = WeightMatrix()

    m.add([2, 3, 4])
    assert m[(2, 3)] == 3
    assert m[(3, 4)] == 3
    assert m[(2, 4)] == 3

    m.add([3, 4])
    assert m[(2, 3)] == 3
    assert m[(3, 4)] == 5
    assert m[(2, 4)] == 3
