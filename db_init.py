import pymongo
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from zing_product_backend.models import material_setting, tp_auto_assign, containment_model
from zing_product_backend.core import common
from zing_product_backend.core.product_containment import containment_constants
from zing_product_backend.app_db.mes_db_query import get_mat_info
mongo_client_ai02 = pymongo.MongoClient(
    'mongodb://10.10.19.185:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
mongo_client_ai01 = pymongo.MongoClient(
    'mongodb://10.10.19.184:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
mongo_client_shaiapp02 = pymongo.MongoClient('mongodb://admin:393103728a@SHAIAPP02:27017')


async def load_mat_info(usr, session: AsyncSession):
    data_dict_list = list(mongo_client_shaiapp02.data_view_site_config_db.mat_alias.find({}))
    df = pd.DataFrame(data=data_dict_list).iloc[:1000, :]
    df = df[~df['matAlias'].isin(['not_allocated', 'not_auto_allocated', 'toEdit'
                                   't',])]
    mat_group_name_list = df['matAlias'].unique().tolist()
    for mat_group_name in mat_group_name_list:
        mat_group_orm = material_setting.MatGroupDef(
            group_name=mat_group_name, group_type=common.MatGroupType.YIELD_GROUP, created_by=usr.user_name,
            updated_by=usr.user_name
        )
        group_df = df[df['matAlias'] == mat_group_name]
        for _index, data_row in group_df.iterrows():
            mat_id = data_row['materialId']
            mat_type = data_row['materialType']
            if mat_type == 'ingot':
                mat_type = common.MatBaseType.GROWING
            elif mat_type == 'wafering':
                mat_type = common.MatBaseType.WAFERING

            assert mat_type in [common.MatBaseType.GROWING, common.MatBaseType.WAFERING]
            try:
                mat_info_dict = get_mat_info(mat_id)
                mat_orm = material_setting.MatDef(
                    mat_id=mat_id, mat_base_type=mat_type,
                    updated_by=usr.user_name,
                    mat_description=mat_info_dict['mat_desc'],
                    mat_type=mat_info_dict['mat_type'],
                    mat_grp_1=mat_info_dict['mat_grp_1'],
                    mat_grp_2=mat_info_dict['mat_grp_2'],
                    mat_grp_3=mat_info_dict['mat_grp_3'],
                    mat_grp_4=mat_info_dict['mat_grp_4'],
                    mat_grp_5=mat_info_dict['mat_grp_5'],
                    mat_grp_6=mat_info_dict['mat_grp_6'],
                    mat_grp_7=mat_info_dict['mat_grp_7'],
                    mat_grp_8=mat_info_dict['mat_grp_8'],
                    mat_cmf_1=mat_info_dict['mat_cmf_1'],
                    mat_cmf_2=mat_info_dict['mat_cmf_2'],
                    mat_cmf_3=mat_info_dict['mat_cmf_3'],
                    mat_cmf_4=mat_info_dict['mat_cmf_4'],
                    def_qty_1=mat_info_dict['def_qty_1'],
                    def_qty_2=mat_info_dict['def_qty_2'],
                    def_qty_3=mat_info_dict['def_qty_3'],
                    first_flow=mat_info_dict['first_flow'],
                    delete_flag=(mat_info_dict['delete_flag'] == 'Y')
                )
                mat_group_orm.materials.append(mat_orm)
            except AssertionError:
                print(rf'assertion error for mat_id {mat_id}')
        session.add(mat_group_orm)
    await session.commit()


async def init_containment_base_rule(usr, session: AsyncSession):
    for entry in containment_constants.BaseRuleName:
        rule_orm = containment_model.ContainmentBaseRule(
            rule_name=entry.value, rule_type=entry.name, created_by=usr.user_name, updated_by=usr.user_name
        )
        session.add(rule_orm)