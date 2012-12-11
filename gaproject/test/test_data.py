
import pytest
from gaproject.data import Box, Data


def test_box():
    box = Box('data/TSPBenchmark')
    data = box.get('belgiumtour.tsp')
    assert data is not None


@pytest.fixture
def belgiumtour_data():
    box = Box('data/TSPBenchmark')
    return box.get('belgiumtour.tsp')


def test_positions(belgiumtour_data):
    assert belgiumtour_data.positions is not None


def test_matrix(belgiumtour_data):
    assert belgiumtour_data.dist_matrix() is not None
