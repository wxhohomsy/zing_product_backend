from typing import TYPE_CHECKING
from sqlalchemy import text
from zing_product_backend.core.product_containment.containment_constants import ContainmentBaseRuleClass
from zing_product_backend.reporting import system_log
from zing_product_backend.core.product_containment.containment_base_rules.containment_mesdb_query import *
from ...parser_core.result_structure import ContainmentResult, ContainmentStatus, ContainmentDetailData
if TYPE_CHECKING:
    from ...parser_core.containment_structure import ContainmentBaseRule, Product


def mesdb_table_main(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert base_rule.rule_class in [ContainmentBaseRuleClass.MWIPMATDEF, ContainmentBaseRuleClass.MWIPLOTSTS,
                                    ContainmentBaseRuleClass.MWIPSLTSTS]
    if base_rule.rule_class == ContainmentBaseRuleClass.MWIPMATDEF:
        return check_mwipmatdef_rule(base_rule, target_product)
    elif base_rule.rule_class == ContainmentBaseRuleClass.MWIPLOTSTS:
        return check_mwiplotsts_rule(base_rule, target_product)
    elif base_rule.rule_class == ContainmentBaseRuleClass.MWIPSLTSTS:
        return check_mwipsltsts_rule(base_rule, target_product)


def check_mwipmatdef_rule(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    target_product_mat = get_material_from_product(target_product)
    base_rule_sql = base_rule.rule_sql
    sql = text(rf"""
        SELECT 1 FROM MESMGR.mwipmatdef
        WHERE 1 = 1
        AND MAT_ID = '{target_product_mat}'
        AND {base_rule_sql}
    """)
    system_log.server_logger.log(f"check_mwipmatdef_rule for {target_product.id}: {sql}")
    with get_cdb_engine(target_product.virtual_factory).connect() as c:
        result = c.execute(sql).fetchone()
        if result:
            result_status = ContainmentStatus.PASS
        else:
            result_status = ContainmentStatus.CATCH

        detail_data = ContainmentDetailData(base_rule=base_rule, target_object=target_product,
                                            result_status=result_status, actual_value=str(sql))
        return ContainmentResult(result_status=result_status, target_object=target_product,
                                 detail_data_list=[detail_data])


def check_mwipsltsts_rule(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    base_rule_sql = base_rule.rule_sql
    sql = text(rf"""
        SELECT 1 FROM MESMGR.mwipsltsts
        WHERE 1 = 1
        AND {base_rule_sql}
    """)
    with get_cdb_engine(target_product.virtual_factory).connect() as c:
        result = c.execute(sql).fetchone()
        if result:
            result_status = ContainmentStatus.PASS
        else:
            result_status = ContainmentStatus.CATCH

        detail_data = ContainmentDetailData(base_rule=base_rule, target_object=target_product,
                                            result_status=result_status, actual_value=str(sql))
        return ContainmentResult(result_status=result_status, target_object=target_product,
                                 detail_data_list=[detail_data])


def check_mwiplotsts_rule(base_rule: 'ContainmentBaseRule', target_product: 'Product') -> ContainmentResult:
    assert isinstance(target_product, LotLikeProduct), rf"target_product must be LotLikeProduct, not {target_product}"
    base_rule_sql = base_rule.rule_sql
    sql = text(rf"""
        SELECT 1 FROM MESMGR.mwiplotsts
        WHERE 1 = 1
        AND {base_rule_sql}
    """)
    with get_cdb_engine(target_product.virtual_factory).connect() as c:
        result = c.execute(sql).fetchone()
        if result:
            result_status = ContainmentStatus.PASS
        else:
            result_status = ContainmentStatus.CATCH

        detail_data = ContainmentDetailData(base_rule=base_rule, target_object=target_product,
                                            result_status=result_status, actual_value=str(sql))
        return ContainmentResult(result_status=result_status, target_object=target_product,
                                 detail_data_list=[detail_data])

