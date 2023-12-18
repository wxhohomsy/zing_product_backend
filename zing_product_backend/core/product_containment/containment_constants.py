from enum import Enum
from typing import Union, Literal, List

t_value_source = Literal['field', 'value']


class ContainmentStatus(Enum):
    PASS = 'PASS'
    CATCH = 'CATCH'
    FAILED = 'FAILED'


class BaseRuleType(str, Enum):
    DB_TABLE = 'db_table'
    CUSTOM_FUNCTION = 'custom_function'


class BaseRuleName(Enum):
    SPC_OOS = 'spc_oos'
    SPC_OOC = 'spc_ooc'
    MWIPSLTSTS = 'mwipsltsts'
    MWIPLOTSTS = 'mwiplotsts'
    MWIPMATDEF = 'mwipmatdef'
    PS_DELTA_TO_TARGET = 'ps_delta_to_target'
    PS_DELTA_TO_MOVING_AVG = 'ps_delta_to_moving_avg'
    YIELD_MAT_GROUP = 'yield_mat_group'


class BaseRuleParaType(Enum):
    FLOAT = 'float'
    INT = 'int'
    STRING = 'string'
    REGEX_PATTERN = 'regex_pattern'


class BaseRuleOperator(Enum):
    BETWEEN = 'between'
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    EQUAL = '='
    NOT_EQUAL = '!='
    CONTAINS = 'contains'
    NOT_CONTAINS = 'not_contains'
    NOT_BETWEEN = 'not_between'
    IN = 'in'
    NOT_IN = 'not_in'


# ------------------ growing FDC related -----------------------------------------
class FdcBaseRuleName(Enum):
    PS2H_DELTA_TO_MOVING_AVG = 'ps_2h_delta_TO_moving_avg'
    PS2H_DELTA_TO_TARGET = 'ps_2h_delta_to_target'
    TARGET_PS = 'target_ps'
