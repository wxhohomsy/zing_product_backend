import pytest
import pandas as pd
from zing_product_backend.app_db import mes_db_query


class Fruit:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name


@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


@pytest.fixture
def app():
    return 1


def test_my_fruit_in_basket(app):
    assert app == 1


def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4