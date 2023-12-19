from typing import Tuple, List, Literal
from zing_product_backend.core.settings import CHAR_DATA_VIRTUAL_LIMIT


def change_limit_to_float(raw_value, type_name: Literal['lower', 'upper']):
    """
    change spec bound to float, give empty bound a large number to make char in SPEC
    """

    assert type(raw_value) == str, fr'raw_value: {raw_value} not as expected, has type {type(raw_value)}'
    if raw_value == ' ':
        if type_name == 'lower':
            return -CHAR_DATA_VIRTUAL_LIMIT
        elif type_name == 'upper':
            return CHAR_DATA_VIRTUAL_LIMIT
        else:
            raise NameError(fr'type_name: {type_name} not as expected')

    else:
        return float(raw_value)


def change_str_to_boolean(raw_value):
    assert type(raw_value) in [str, type(None)], fr'raw_value: {raw_value} not as expected, has type {type(raw_value)}'
    if raw_value == 'Y':
        return True
    else:
        return False
