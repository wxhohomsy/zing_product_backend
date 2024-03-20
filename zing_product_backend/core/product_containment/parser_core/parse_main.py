from enum import Enum
from typing import Dict, Tuple, List, Union
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core import common
from . import containment_structure, result_structure
from zing_product_backend.core.product_containment.containment_base_rules import m1_fdc


def get_available_operators_and_fields(containment_base_rule_class_name: ContainmentBaseRuleClass) -> Tuple[Enum, Enum]:
    if containment_base_rule_class_name == ContainmentBaseRuleClass.INGOT_FDC:
        return_operator_enum = IngotFdcOperator
        return_operator_field_enum = IngotFdcField
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.CRYSTAL_EQUIP:
        return_operator_enum = CrystalEquipOperator
        return_operator_field_enum = CrystalEquipField
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.CRYSTAL_DEFECT:
        return_operator_enum = CrystalDefectOperator
        return_operator_field_enum = CrystalDefectField
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.TIME_RELATED:
        return_operator_enum = TimeRelatedOperator
        return_operator_field_enum = TimeRelatedField
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.MAT_GROUP:
        return_operator_enum = MatGroupOperator
        return_operator_field_enum = MatGroupField
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.SPC_OOS:
        return_operator_enum = SpcOosOperators
        return_operator_field_enum = None
    elif containment_base_rule_class_name == ContainmentBaseRuleClass.SPC_OOC:
        return_operator_enum = SpcOosOperators
        return_operator_field_enum = None

    elif containment_base_rule_class_name == ContainmentBaseRuleClass.SPC_VALUE:
        return_operator_enum = SpcValueOperators
        return_operator_field_enum = None

    elif containment_base_rule_class_name in [ContainmentBaseRuleClass.MWIPLOTSTS, ContainmentBaseRuleClass.MWIPSLTSTS,
                                              ContainmentBaseRuleClass.MWIPMATDEF,
                                              ContainmentBaseRuleClass.MESDB_CUSTOM_SQL
                                              ]:
        return_operator_enum = None
        return_operator_field_enum = None

    else:
        raise ValueError(f"Unknown containment base rule class: {containment_base_rule_class_name}")

    return return_operator_enum, return_operator_field_enum


def parser_function(rule_name):
    sw
    pass


def parse_base_rule_main(target_object, rule_data: Dict, rule_class: ContainmentBaseRuleClass, rule_object) -> \
        result_structure.ContainmentResult:

    pass


