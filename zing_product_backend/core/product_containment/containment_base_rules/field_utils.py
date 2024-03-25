from typing import Union
from ..containment_constants import NumericOperator, MultiFieldOperator


def change_field_value_to_float(field_value: Union[str, float, list[str]]) -> Union[float, list[float]]:
    if isinstance(field_value, str):
        return float(field_value)
    elif isinstance(field_value, float):
        return field_value
    elif isinstance(field_value, list):
        return [float(value) for value in field_value]
    else:
        raise ValueError(f'invalid field value {field_value}')


def soft_equal(value: float, target_value: float):
    return abs(value - target_value) < 1e-4


def compute_numeric_field_result(operator: NumericOperator,
                                 field_value: Union[list[float, float], float], value: float) -> bool:
    match operator:
        case NumericOperator.BETWEEN:
            assert type(field_value) is list and len(field_value) == 2, f'invalid field value {field_value}'
            result = field_value[0] <= value <= field_value[1]

        case NumericOperator.EQUAL:
            result = soft_equal(value, field_value)

        case NumericOperator.GT:
            result = value > field_value

        case NumericOperator.GTE:
            result = value >= field_value

        case NumericOperator.LT:
            result = value < field_value

        case NumericOperator.LTE:
            result = value <= field_value

        case NumericOperator.NOT_EQUAL:
            result = not soft_equal(value, field_value)

        case NumericOperator.NOT_BETWEEN:
            assert type(field_value) is list and len(field_value) == 2, f'invalid field value {field_value}'
            result = not (field_value[0] <= value <= field_value[1])

        case _:
            raise ValueError(f'unsupported operator {operator}')

    return result


def computer_select_field_result(operator: MultiFieldOperator, field_value: list[str]) -> bool:
    match operator:
        case MultiFieldOperator.IN:
            return field_value in field_value
        case MultiFieldOperator.NOT_IN:
            return field_value not in field_value
        case _:
            raise ValueError(f'unsupported operator {operator}')
