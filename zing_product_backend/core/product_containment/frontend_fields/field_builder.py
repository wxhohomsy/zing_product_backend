import typing
from decimal import Decimal
import warnings
from typing import List, Union, Tuple, Type
from sqlalchemy import text, inspect, Table
from sqlalchemy.orm import DeclarativeBase
from zing_product_backend.app_db import mes_db_query
from zing_product_backend.core.product_containment.containment_constants import *
from zing_product_backend.core.product_containment import crud
from zing_product_backend.core import exceptions
from . import fields_schema
from zing_product_backend.core import common
if typing.TYPE_CHECKING:
    from zing_product_backend.models import general_settings


async def build_fields_from_sql_rule(db_table: Union[Table, Type[DeclarativeBase]]) -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    for col in inspect(db_table).columns:
        input_type: RuleInputType = None
        value_editor_type: RuleValueEditor = RuleValueEditor.TEXT
        if issubclass(col.type.python_type, (Decimal, float, int)):
            input_type = RuleInputType.NUMBER
        elif issubclass(col.type.python_type, str):
            input_type = RuleInputType.TEXT
        elif issubclass(col.type.python_type, bool):
            input_type = RuleInputType.CHECKBOX
            value_editor_type = RuleValueEditor.CHECKBOX
        else:
            warnings.warn(f'Unknown type {col.type} for column {col.name}')
            print(col.type.python_type)

        to_return_field_list.append(fields_schema.Field(
            name=col.name,
            inputType=input_type,
            valueEditorType=value_editor_type,
        ))

    return to_return_field_list


async def build_custom_sql_fields() -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    operators = [fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=2)  \
                 for operator in CustomSqlOperator]
    for field_name in CustomSqlField:
        to_return_field_list.append(fields_schema.Field(
            name=field_name,
            inputType=RuleInputType.TEXT,
            valueEditorType=RuleValueEditor.TEXT,
            operators=operators,
        ))
    return to_return_field_list


async def build_spc_fields(base_rule_class: ContainmentBaseRuleClass,
                           virtual_factory: common.VirtualFactory)-> List[fields_schema.Field]:
    operator_list = []
    if base_rule_class in [ContainmentBaseRuleClass.SPC_OOC, ContainmentBaseRuleClass.SPC_OOS]:
        for operator_name in SpcOosOperators:
            operator_list.append(fields_schema.RuleOperator(name=operator_name, label=operator_name, arity=0))
        input_type = RuleInputType.CHECKBOX
        value_editor_type = RuleValueEditor.CHECKBOX

    elif base_rule_class == ContainmentBaseRuleClass.SPC_VALUE:
        for operator in SPC_VALUE_OPERATOR_NAMES:
            if operator in (RuleOperatorName.BETWEEN, RuleOperatorName.NOT_BETWEEN):
                arity = 3
            else:
                arity = 2
            operator_list.append(
                fields_schema.RuleOperator(name=operator, label=operator, arity=arity)
            )
        input_type = RuleInputType.NUMBER
        value_editor_type = RuleValueEditor.TEXT
    else:
        raise ValueError(f'Invalid base rule class {base_rule_class}')

    field_list: List[fields_schema.Field] = []
    oper_list = mes_db_query.get_available_oper_id_list('2100', '6898', virtual_factory)

    for oper_id in oper_list:
        field_list.append(fields_schema.Field(
            name=oper_id,
            label=oper_id,
            inputType=input_type,
            valueEditorType=value_editor_type,
            operators=operator_list,
        ))
    return field_list


async def build_time_related_field()-> List[fields_schema.Field]:
    field_list: List[fields_schema.Field] = []
    operator_list = []
    for operator in CrystalEquipOperator:
        if operator in (RuleOperatorName.BETWEEN, RuleOperatorName.NOT_BETWEEN):
            arity = 3
        else:
            arity = 2
        operator_list.append(fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=arity))
    for file_name in TimeRelatedField:
        field_list.append(fields_schema.Field(
            name=file_name,
            label=file_name,
            inputType=RuleInputType.DATETIME_LOCAL,
            valueEditorType=RuleValueEditor.TEXT,
        ))
    return field_list


async def build_crystal_equip_field() -> List[fields_schema.Field]:
    to_return_field_list = []
    puller_info_list: List['general_settings.PullerInfo'] = await crud.get_available_puller_info_list()
    puller_name_list = [puller_info.puller_name for puller_info in puller_info_list]
    puller_mes_id_list = [puller_info.puller_mes_id for puller_info in puller_info_list]
    operator_list = []
    for operator in CrystalEquipOperator:
        operator_list.append(fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=2))

    puller_name_values: fields_schema.RuleValues = [
        fields_schema.RuleValues(name=puller_name, label=puller_name) for puller_name in puller_name_list
    ]
    puller_mes_id_values: fields_schema.RuleValues = [
        fields_schema.RuleValues(name=puller_mes_id, label=puller_mes_id) for puller_mes_id in puller_mes_id_list
        ]
    v_factory_values: fields_schema.RuleValues = [
        fields_schema.RuleValues(name=virtual_factory, label=virtual_factory) for virtual_factory in
        [common.VirtualFactory.L1W, common.VirtualFactory.L2W, common.VirtualFactory.ALL]
    ]
    for field_name in CrystalEquipField:
        if field_name == CrystalEquipField.PULLER_NAME:
            field = fields_schema.Field(
                name=field_name,
                label=field_name,
                valueEditorType=RuleValueEditor.MULTISELECT,
                values=puller_name_values,
                valueSources=['value'],
                operators=operator_list,
            )
            to_return_field_list.append(field)
        elif field_name == CrystalEquipField.PULLER_MES_ID:
            field = fields_schema.Field(
                name=field_name,
                label=field_name,
                valueEditorType=RuleValueEditor.MULTISELECT,
                values=puller_mes_id_values,
                valueSources=['value'],
                operators=operator_list,
            )
            to_return_field_list.append(field)
        elif field_name == CrystalEquipField.VIRTUAL_FACTORY:
            field = fields_schema.Field(
                name=field_name,
                label=field_name,
                valueEditorType=RuleValueEditor.MULTISELECT,
                values=v_factory_values,
                valueSources=['value'],
                operators=operator_list,
            )
            to_return_field_list.append(field)
        else:
            raise exceptions.NotFoundError(f'Unknown field name {field_name} for growing equip rule class')
    return to_return_field_list


async def build_ingot_fdc_field()-> List[fields_schema.Field]:
    to_return_field_list = []
    operator_list = []
    for operator in IngotFdcOperator:
        operator_list.append(fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=2))
    for field_name in IngotFdcField:
        field = fields_schema.Field(
            name=field_name,
            label=field_name,
            valueEditorType=RuleValueEditor.TEXT,
            inputType=RuleInputType.NUMBER,
            operators=operator_list,
        )
        to_return_field_list.append(field)
    return to_return_field_list


async def build_mat_group_field() -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    operator_list: List[fields_schema.RuleOperator] = []
    for operator in MatGroupOperator:
        operator_list.append(fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=2))

    for field_name in MatGroupField:
        if field_name == MatGroupField.YIELD_MAT_GROUP:
            mat_yield_group_names = await crud.get_mat_yield_group_names()
            mat_yield_group_values: fields_schema.RuleValues = [
                fields_schema.RuleValues(name=mat_yield_group_name, label=mat_yield_group_name) for
                mat_yield_group_name in mat_yield_group_names
            ]
            field = fields_schema.Field(
                name=field_name,
                label=field_name,
                valueEditorType=RuleValueEditor.MULTISELECT,
                inputType=RuleInputType.TEXT,
                values=mat_yield_group_values,
                valueSources=['value'],
                operators=operator_list,
            )
            to_return_field_list.append(field)
        else:
            raise exceptions.NotImplementError(f'Unknown field name {field_name} for mat_group class')
    return to_return_field_list


async def build_crystal_defect_field() -> List[fields_schema.Field]:
    to_return_field_list: List[fields_schema.Field] = []
    operator_list: List[fields_schema.RuleOperator] = []
    for operator in CrystalDefectOperator:
        operator_list.append(fields_schema.RuleOperator(name=operator.value, label=operator.value, arity=2))

    for field_name in CrystalDefectField:
        to_return_field_list.append(
            fields_schema.Field(
                name=field_name,
                label=field_name,
                valueEditorType=RuleValueEditor.TEXT,
                inputType=RuleInputType.NUMBER,
                operators=operator_list,
            )
        )
    return to_return_field_list


async def build_fields_from_custom_rule(base_rule_class: ContainmentBaseRuleClass,
                                        virtual_factory: common.VirtualFactory):
    if base_rule_class in [ContainmentBaseRuleClass.SPC_OOC, ContainmentBaseRuleClass.SPC_OOS,
                           ContainmentBaseRuleClass.SPC_VALUE]:
        return await build_spc_fields(base_rule_class, virtual_factory)
    elif base_rule_class == ContainmentBaseRuleClass.CRYSTAL_EQUIP:
        return await build_crystal_equip_field()

    elif base_rule_class == ContainmentBaseRuleClass.TIME_RELATED:
        return await build_time_related_field()

    elif base_rule_class == ContainmentBaseRuleClass.INGOT_FDC:
        return await build_ingot_fdc_field()

    elif base_rule_class == ContainmentBaseRuleClass.MAT_GROUP:
        return await build_mat_group_field()

    elif base_rule_class == ContainmentBaseRuleClass.CRYSTAL_DEFECT:
        return await build_crystal_defect_field()

    elif base_rule_class == ContainmentBaseRuleClass.MESDB_CUSTOM_SQL:
        return await build_custom_sql_fields()

    else:
        warnings.warn(f'Unknown rule class {base_rule_class}')
        return []


