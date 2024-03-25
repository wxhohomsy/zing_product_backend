import pymongo
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from zing_product_backend.models import general_settings, tp_auto_assign, containment_model
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
        mat_group_orm =general_settings.MatGroupDef(
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
                mat_orm = general_settings.MatDef(
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


async def load_puller_info(session: AsyncSession):
    data_list = [
        ['N01', 'AGGRN01', 'L1W', 11, 'NAST'],
        ['N02', 'AGGRN02', 'L1W', 12, 'NAST'],
        ['N03', 'AGGRN03', 'L1W', 13, 'NAST'],
        ['J01', 'BGGRJ01', 'L1W', 52, 'JS'],
        ['J02', 'BGGRJ02', 'L2W', 51, 'JS'],
        ['J03', 'BGGRJ03', 'L2W', 50, 'JS'],
        ['S01', 'AGGRS01', 'L1W', 1, 'STECH'],
        ['S02', 'AGGRS02', 'L1W', 2, 'STECH'],
        ['S03', 'AGGRS03', 'L1W', 3, 'STECH'],
        ['S04', 'AGGRS04', 'L1W', 4, 'STECH'],
        ['S05', 'AGGRS05', 'L1W', 5, 'STECH'],
        ['S06', 'AGGRS06', 'L1W', 6, 'STECH'],
        ['S07', 'AGGRS07', 'L1W', 7, 'STECH'],
        ['S08', 'AGGRS08', 'L1W', 8, 'STECH'],
        ['S09', 'AGGRS09', 'L1W', 9, 'STECH'],
        ['S10', 'AGGRS10', 'L1W', 10, 'STECH'],
        ['S11', 'AGGRS11', 'L1W', 14, 'STECH'],
        ['S12', 'AGGRS12', 'L1W', 15, 'STECH'],
        ['S13', 'AGGRS13', 'L1W', 16, 'STECH'],
        ['S14', 'AGGRS14', 'L1W', 17, 'STECH'],
        ['S15', 'AGGRS15', 'L1W', 18, 'STECH'],
        ['S16', 'AGGRS16', 'L1W', 19, 'STECH'],
        ['S17', 'AGGRS17', 'L1W', 20, 'STECH'],
        ['S18', 'AGGRS18', 'L1W', 21, 'STECH'],
        ['S19', 'AGGRS19', 'L1W', 22, 'STECH'],
        ['S20', 'AGGRS20', 'L1W', 23, 'STECH'],
        ['S21', 'AGGRS21', 'L1W', 24, 'STECH'],
        ['S22', 'AGGRS22', 'L1W', 25, 'STECH'],
        ['S23', 'AGGRS23', 'L1W', 26, 'STECH'],
        ['S24', 'AGGRS24', 'L1W', 27, 'STECH'],
        ['S25', 'AGGRS25', 'L1W', 28, 'STECH'],
        ['S26', 'BGGRS01', 'L1W', 29, 'STECH'],
        ['S27', 'BGGRS02', 'L1W', 30, 'STECH'],
        ['S28', 'BGGRS03', 'L1W', 31, 'STECH'],
        ['S29', 'BGGRS04', 'L1W', 32, 'STECH'],
        ['S30', 'BGGRS05', 'L1W', 33, 'STECH'],
        ['S31', 'BGGRS06', 'L1W', 34, 'STECH'],
        ['S32', 'BGGRS07', 'L1W', 35, 'STECH'],
        ['S33', 'BGGRS08', 'L2W', 36, 'STECH'],
        ['S34', 'BGGRS09', 'L2W', 37, 'STECH'],
        ['S35', 'BGGRS10', 'L2W', 38, 'STECH'],
        ['S36', 'BGGRS11', 'L2W', 39, 'STECH'],
        ['S37', 'BGGRS12', 'L2W', 40, 'STECH'],
        ['S38', 'BGGRS13', 'L2W', 41, 'STECH'],
        ['S39', 'BGGRS14', 'L2W', 42, 'STECH'],
        ['S40', 'BGGRS15', 'L2W', 43, 'STECH'],
        ['S41', 'BGGRS16', 'L2W', 44, 'STECH'],
        ['S42', 'BGGRS17', 'L2W', 45, 'STECH'],
        ['S43', 'BGGRS18', 'L2W', 46, 'STECH'],
        ['S44', 'BGGRS19', 'L2W', 47, 'STECH'],
        ['S45', 'BGGRS20', 'L2W', 48, 'STECH'],
        ['S46', 'BGGRS21', 'L2W', 49, 'STECH'],
    ]

    for data in data_list:
        puller_name, mes_id, virtual_factory, mes_index, puller_type = data
        puller_orm = general_settings.PullerInfo(
            puller_name=puller_name, puller_mes_id=mes_id, virtual_factory=virtual_factory,
            puller_type=puller_type, puller_mes_index=mes_index, owner_name='admin'
        )

        session.add(puller_orm)
    await session.commit()