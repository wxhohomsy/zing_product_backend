from enum import Enum
from typing import Union, Literal, List
from zing_product_backend.app_db.external_tables import mwiplotsts_l1w, mwipsltsts_l1w, mwipmatdef_l1w
t_value_source = Literal['field', 'value']


class ProductObjectType(str, Enum):
    SUBLOT = 'sublot'
    LOT = 'lot'
    WAFERING_SEGMENT = 'wafering_segment'
    GROWING_SEGMENT = 'growing_segment'
    INGOT = 'ingot'


class RuleGroupType(Enum):
    RULE = 'rule'
    RULE_GROUP = 'rule_group'


class ContainmentStatus(Enum):
    PASS = 'pass'
    CATCH = 'catch'
    UNKNOWN = 'unknown'


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


class RuleOperatorName(Enum):
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
    CRYSTAL_EQUIP = 'crystal_equip'
    TIME_RELATED = 'time_related'
    CRYSTAL_DEFECT = 'crystal_defect'
    INGOT_FDC = 'ingot_fdc'
    MAT_GROUP = 'mat_group'
    MESDB_CUSTOM_SQL = 'mesdb_custom_sql'
    MWIPSLTSTS = 'mwipsltsts'
    MWIPLOTSTS = 'mwiplotsts'
    MWIPMATDEF = 'mwipmatdef'


# -------------------------------- rule config related -------------------------------
RULE_IS_SQL_DICT = {
    ContainmentBaseRuleClass.SPC_OOS: False,
    ContainmentBaseRuleClass.SPC_OOC: False,
    ContainmentBaseRuleClass.SPC_VALUE: False,
    ContainmentBaseRuleClass.CRYSTAL_EQUIP: False,
    ContainmentBaseRuleClass.TIME_RELATED: False,
    ContainmentBaseRuleClass.CRYSTAL_DEFECT: False,
    ContainmentBaseRuleClass.INGOT_FDC: False,
    ContainmentBaseRuleClass.MAT_GROUP: False,
    ContainmentBaseRuleClass.MESDB_CUSTOM_SQL: False,
    ContainmentBaseRuleClass.MWIPSLTSTS: True,
    ContainmentBaseRuleClass.MWIPLOTSTS: True,
    ContainmentBaseRuleClass.MWIPMATDEF: True,
}

RULE_IS_SPC_DICT = {
    ContainmentBaseRuleClass.SPC_OOS: True,
    ContainmentBaseRuleClass.SPC_OOC: True,
    ContainmentBaseRuleClass.SPC_VALUE: True,
    ContainmentBaseRuleClass.CRYSTAL_EQUIP: False,
    ContainmentBaseRuleClass.TIME_RELATED: False,
    ContainmentBaseRuleClass.CRYSTAL_DEFECT: False,
    ContainmentBaseRuleClass.INGOT_FDC: False,
    ContainmentBaseRuleClass.MAT_GROUP: False,
    ContainmentBaseRuleClass.MESDB_CUSTOM_SQL: False,
    ContainmentBaseRuleClass.MWIPSLTSTS: False,
    ContainmentBaseRuleClass.MWIPLOTSTS: False,
    ContainmentBaseRuleClass.MWIPMATDEF: False,
}

# we focus on columns and type, so l1w table is assumed to be same as l2w table, but bug may still lurks
RULE_SQL_TABLE_MAPPING = {
    ContainmentBaseRuleClass.MWIPSLTSTS:  mwipsltsts_l1w,
    ContainmentBaseRuleClass.MWIPLOTSTS: mwiplotsts_l1w,
    ContainmentBaseRuleClass.MWIPMATDEF: mwipmatdef_l1w,
}


# ------------------ SPC related -----------------------------------------
ALL_SPEC = 'all_spec'


class SpcOosOperators(Enum):
    OK = 'ok'
    NG = 'ng'
    UNKNOWN = 'unknown'


class SpcSpecialSpec(Enum):
    ALL_SPEC = 'all_spec'
    ANY_SPEC = 'any_spec'


SPC_VALUE_OPERATOR_NAMES = [RuleOperatorName.BETWEEN, RuleOperatorName.NOT_BETWEEN, RuleOperatorName.GT,
                            RuleOperatorName.GTE, RuleOperatorName.LT, RuleOperatorName.LTE]


# ------------------------- time related -----------------------------------------------------
class TimeRelatedField(Enum):
    EXECUTE_TIME = 'execute_time'
    CREATE_TIME = 'create_time'


class TimeRelatedOperator(Enum):
    BETWEEN = RuleOperatorName.BETWEEN
    NOT_BETWEEN = RuleOperatorName.NOT_BETWEEN
    GT = RuleOperatorName.GT
    GTE = RuleOperatorName.GTE
    LT = RuleOperatorName.LT
    LTE = RuleOperatorName.LTE


# -------------------------- ingot fdc --------------------------------------------------------
class IngotFdcField(Enum):
    PS_2H_SHIFT_50MM = 'ps_2h_shift_50mm'
    DIAMETER = 'diameter'
    DELTA_PS2H50MM_TO_TARGET = 'delta_ps_2H_50mm_to_target'
    DELTA_PS2H50MM_TO_MOVING_AVG = 'delta_ps_2H_50mm_to_moving_avg'


class IngotFdcOperator(Enum):
    BETWEEN = RuleOperatorName.BETWEEN
    NOT_BETWEEN = RuleOperatorName.NOT_BETWEEN
    GT = RuleOperatorName.GT
    GTE = RuleOperatorName.GTE
    LT = RuleOperatorName.LT
    LTE = RuleOperatorName.LTE
# -------------------------- crystal_equip  --------------------------------------------------------


class CrystalEquipField(Enum):
    PULLER_NAME = 'puller_name'
    PULLER_MES_ID = 'puller_mes_id'
    VIRTUAL_FACTORY = 'virtual_factory'


class CrystalEquipOperator(Enum):
    IN = RuleOperatorName.IN
    NOT_IN = RuleOperatorName.NOT_IN
    EQUAL = RuleOperatorName.EQUAL
    NOT_EQUAL = RuleOperatorName.NOT_EQUAL


# -------------------------------------- mat group -----------------------------------------------------
class MatGroupField(Enum):
    YIELD_MAT_GROUP = 'yield_mat_group'


class MatGroupOperator(Enum):
    IN = RuleOperatorName.IN
    NOT_IN = RuleOperatorName.NOT_IN


# -------------------------------------- crystal defect -----------------------------------------------------
class CrystalDefectOperator(Enum):
    BETWEEN = RuleOperatorName.BETWEEN
    NOT_BETWEEN = RuleOperatorName.NOT_BETWEEN
    GT = RuleOperatorName.GT
    GTE = RuleOperatorName.GTE
    LT = RuleOperatorName.LT
    LTE = RuleOperatorName.LTE
    EQUAL = RuleOperatorName.EQUAL


class CrystalDefectField(Enum):
    LINEAR_PV = 'linear_pv'
    LINEAR_A_DEFECT = 'linear_a_defect'
    LINEAR_A_DENSITY = 'linear_a_density'
    LINEAR_COP19 = 'linear_cop19'
    LINEAR_COP26 = 'linear_cop26'
    LINEAR_COP37 = 'linear_cop37'
    LINEAR_DWO_ALL = 'linear_dwo_all'
    LINEAR_DWO_CENTER = 'linear_dwo_center'
    LINEAR_DWO_EDGE = 'linear_dwo_edge'
    LEFT_TP_PV = 'left_pv'
    LEFT_TP_A_DEFECT = 'left_a_defect'
    LEFT_TP_COP19 = 'left_cop19'
    LEFT_TP_COP26 = 'left_cop26'
    LEFT_TP_COP37 = 'left_cop37'
    LEFT_TP_DWO_ALL = 'left_dwo_all'
    LEFT_TP_DWO_CENTER = 'left_dwo_center'
    LEFT_TP_DWO_EDGE = 'left_dwo_edge'
    RIGHT_TP_PV = 'right_pv'
    RIGHT_TP_A_DEFECT = 'right_a_defect'
    RIGHT_TP_COP19 = 'right_cop19'
    RIGHT_TP_COP26 = 'right_cop26'
    RIGHT_TP_COP37 = 'right_cop37'
    RIGHT_TP_DWO_ALL = 'right_dwo_all'
    RIGHT_TP_DWO_CENTER = 'right_dwo_center'
    RIGHT_TP_DWO_EDGE = 'right_dwo_edge'


# -------------------------------------- custom sql -----------------------------------------------------
class CustomSqlField(Enum):
    MESDB_SQL = 'mesdb_sql'
    MESETL_DB_SQL = 'mesetl_db_sql'


class CustomSqlOperator(Enum):
    EQUAL = RuleOperatorName.EQUAL
