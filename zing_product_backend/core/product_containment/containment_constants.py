from enum import Enum
from typing import Union, Literal, List

t_value_source = Literal['field', 'value']


class RuleGroupType(Enum):
    RULE = 'rule'
    RULE_GROUP = 'rule_group'


class ContainmentStatus(Enum):
    PASS = 'pass'
    CATCH = 'catch'
    ERROR = 'error'


class BaseRuleType(str, Enum):
    DB_TABLE = 'db_table'
    CUSTOM_FUNCTION = 'custom_function'


class BaseRuleName(Enum):
    SPC_OOS = 'spc_oos'
    SPC_OOC = 'spc_ooc'
    SPC_VALUE = 'spc_value'
    MWIPSLTSTS = 'mwipsltsts'
    MWIPLOTSTS = 'mwiplotsts'
    MWIPMATDEF = 'mwipmatdef'
    INGOT_FDC = 'ingot_fdc'
    YIELD_MAT_GROUP = 'yield_mat_group'


class BaseRuleInputType(Enum):
    QUERY_BUILDER = 'query'
    TREE_SELECT = 'tree_select'


class BaseRuleFieldType(Enum):
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


# -------------------------------- rule config related -------------------------------
RULE_INPUT_TYPE_DICT = {
    BaseRuleName.SPC_OOS: BaseRuleInputType.TREE_SELECT,
    BaseRuleName.SPC_OOC: BaseRuleInputType.TREE_SELECT,
    BaseRuleName.SPC_value: BaseRuleInputType.QUERY_BUILDER,
    BaseRuleName.MWIPSLTSTS: BaseRuleInputType.QUERY_BUILDER,
    BaseRuleName.MWIPLOTSTS: BaseRuleInputType.QUERY_BUILDER,
    BaseRuleName.MWIPMATDEF: BaseRuleInputType.QUERY_BUILDER,
    BaseRuleName.INGOT_FDC: BaseRuleInputType.QUERY_BUILDER,
    BaseRuleName.YIELD_MAT_GROUP: BaseRuleInputType.QUERY_BUILDER,
}


# ------------------ growing FDC related -----------------------------------------
class FdcBaseRuleName(Enum):
    PS2H_DELTA_TO_MOVING_AVG = 'ps_2h_delta_TO_moving_avg'
    PS2H_DELTA_TO_TARGET = 'ps_2h_delta_to_target'
    TARGET_PS = 'target_ps'
