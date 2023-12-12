from enum import Enum


class BaseRuleName(Enum):
    SPC_OOS = 'SPC_OOS'
    SPC_OOC = 'SPC_OOC'
    MWIPSLTSTS = 'MWIPSLTSTS'
    MWIPLOTSTS = 'MWIPLOTSTS'
    MWIPMATDEF = 'MWIPMATDEF'
    PS_DELTA_TO_TARGET = 'PS_DELTA_TO_TARGET'
    PS_DELTA_TO_MOVING_AVG = 'PS_DELTA_TO_MOVING_AVG'
    YIELD_MAT_GROUP = 'YIELD_MAT_GROUP'


