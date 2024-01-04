from enum import Enum
from typing import Union, Literal, List
from zing_product_backend.app_db.external_tables import mwiplotsts_l1w, mwipsltsts_l1w, mwipmatdef_l1w
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


class BaseRuleInputType(Enum):
    QUERY_BUILDER = 'query'
    TREE_SELECT = 'tree_select'


class BaseRuleFieldType(Enum):
    FLOAT = 'float'
    INT = 'int'
    STRING = 'string'
    REGEX_PATTERN = 'regex_pattern'


class RuleOperator(Enum):
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


class RuleInputType(Enum):
    BUTTON = 'button'
    CHECKBOX = 'checkbox'
    COLOR = 'color'
    DATE = 'date'
    DATETIME_LOCAL = 'datetime-local'
    EMAIL = 'email'
    FILE = 'file'
    HIDDEN = 'hidden'
    IMAGE = 'image'
    MONTH = 'month'
    NUMBER = 'number'
    PASSWORD = 'password'
    RADIO = 'radio'
    RANGE = 'range'
    RESET = 'reset'
    SEARCH = 'search'
    SUBMIT = 'submit'
    TEL = 'tel'
    TEXT = 'text'
    TIME = 'time'
    URL = 'url'
    WEEK = 'week'


class RuleValueEditor(Enum):
    # type ValueEditorType = 'text' | 'select' | 'checkbox' | 'radio' | 'textarea' | 'switch' | 'multiselect' | null;
    TEXT = 'text'
    SELECT = 'select'
    CHECKBOX = 'checkbox'
    RADIO = 'radio'
    TEXTAREA = 'textarea'
    SWITCH = 'switch'
    MULTISELECT = 'multiselect'


class ContainmentBaseRuleClass(str, Enum):
    SPC_OOS = 'spc_oos'
    SPC_OOC = 'spc_ooc'
    SPC_VALUE = 'spc_value'
    PULLER_ID = 'puller_id'
    EXECUTE_DATETIME = 'execute_datetime'
    HC_REDUCE_RULE = 'hc_reduce_rule'
    INGOT_FDC = 'ingot_fdc'
    YIELD_MAT_GROUP = 'yield_mat_group'
    MESDB_CUSTOM_SQL = 'mesdb_custom_sql'
    MWIPSLTSTS = 'mwipsltsts'
    MWIPLOTSTS = 'mwiplotsts'
    MWIPMATDEF = 'mwipmatdef'


# -------------------------------- rule config related -------------------------------
RULE_IS_SQL_DICT = {
    ContainmentBaseRuleClass.SPC_OOS: False,
    ContainmentBaseRuleClass.SPC_OOC: False,
    ContainmentBaseRuleClass.SPC_VALUE: False,
    ContainmentBaseRuleClass.PULLER_ID: False,
    ContainmentBaseRuleClass.EXECUTE_DATETIME: False,
    ContainmentBaseRuleClass.HC_REDUCE_RULE: False,
    ContainmentBaseRuleClass.INGOT_FDC: False,
    ContainmentBaseRuleClass.YIELD_MAT_GROUP: False,
    ContainmentBaseRuleClass.MESDB_CUSTOM_SQL: False,
    ContainmentBaseRuleClass.MWIPSLTSTS: True,
    ContainmentBaseRuleClass.MWIPLOTSTS: True,
    ContainmentBaseRuleClass.MWIPMATDEF: True,
}

# we focus on columns and type, so l1w table is assumed to be same as l2w table, but bug may still lurks
RULE_SQL_TABLE_MAPPING = {
    ContainmentBaseRuleClass.MWIPSLTSTS:  mwipsltsts_l1w,
    ContainmentBaseRuleClass.MWIPLOTSTS: mwiplotsts_l1w,
    ContainmentBaseRuleClass.MWIPMATDEF: mwipmatdef_l1w,
}


# ------------------ SPC related -----------------------------------------
