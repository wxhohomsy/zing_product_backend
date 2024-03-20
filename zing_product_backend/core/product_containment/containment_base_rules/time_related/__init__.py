import typing
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass


def time_related_main(base_rule_class: ContainmentBaseRuleClass):
    assert base_rule_class in [ContainmentBaseRuleClass.MAT_GROUP], f'base_rule_class {base_rule_class} not supported'


