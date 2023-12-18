import pandas as pd
from typing import Dict
from sqlalchemy import text
from sqlalchemy.engine.row import RowMapping
from cachetools import cached, TTLCache
from zing_product_backend.app_db.connections import l1w_db_engine, l2w_db_engine
from zing_product_backend.core.common_type import *
from zing_product_backend.core import settings


STS_TTL_CACHE = TTLCache(maxsize=10000, ttl=settings.MES_STS_CACHE_TIME)
SPC_TTL_CACHE = TTLCache(maxsize=10000, ttl=settings.SPC_DATA_CACHE_TIME)


class NotFindInDBError(Exception):
    pass


def get_cdb_engine(factory: t_virtual_factory):
    assert factory in ['WE1', 'L2W'], f'factory {factory} is not supported.'
    if factory == 'WE1':
        return l1w_db_engine
    else:
        return l2w_db_engine


def get_sublot_sts(sublot_id: str, factory: t_virtual_factory):
    cdb_engine = get_cdb_engine(factory)
    with cdb_engine.connect() as c:
        sql = text(f"select * from MESMGR.MWIPSLTSTS where SUBLOT_ID = '{sublot_id}'")
        data = c.execute(sql).fetchone()
        if data is None:
            raise NotFindInDBError(sql)
        else:
            return data._mapping


def get_lot_sts(lot_id: str, factory: t_virtual_factory):
    cdb_engine = get_cdb_engine(factory)
    with cdb_engine.connect() as c:
        sql = text(f"select * from MESMGR.MWIPLOTSTS where LOT_ID = '{lot_id}'")
        data = c.execute(sql).fetchone()
        if data is None:
            raise NotFindInDBError(sql)
        else:
            return data._mapping



def create_sql_tuple(str_list: List[str]):
    return tuple([f"'{item}'" for item in str_list])


def get_lot_wip_information(lot_id: str, factory: t_virtual_factory):
    pass


def get_mat_info(mat_id: str) -> Dict:
    with get_cdb_engine('L2W').connect() as c:
        df = pd.read_sql(text(f"select * from MESMGR.MWIPMATDEF where MAT_ID = '{mat_id}'"), c)

    if len(df) == 0:
        with get_cdb_engine('WE1').connect() as c:
            df = pd.read_sql(text(f"select * from MESMGR.MWIPMATDEF where MAT_ID = '{mat_id}'"), c)

    assert len(df) == 1, rf"mat_id {mat_id} is not unique or not none"

    return df.iloc[0, :].to_dict()


def get_spec_by_material_and_operation(mat_id, operation_id_list, virtual_facotry: t_virtual_factory):
    cdb_engine = get_cdb_engine(mat_id[:3])
    sql = text(f"""
    WITH MAT_LIST AS
 (SELECT A.MAT_CMF_1, A.MAT_ID, A.MAT_VER, B.FLOW, C.OPER
    FROM MESMGR.MWIPMATDEF A, MESMGR.MWIPMATFLW B, MESMGR.MWIPFLWOPR C
   WHERE 1 = 1
     AND A.MAT_ID = '3P21XPR246R'
     AND C.OPER IN 
--      AND A.DEACTIVE_FLAG <> 'Y'
     AND A.DELETE_FLAG <> 'Y'
     AND A.MAT_ID = B.MAT_ID(+)
     AND A.MAT_VER = B.MAT_VER(+)
     AND B.FLOW = C.FLOW(+)
     AND FIRST_FLOW <> ' '
     AND A.FIRST_FLOW = B.FLOW(+)
   ORDER BY A.MAT_ID, A.MAT_VER, B.FLOW_SEQ_NUM, C.SEQ_NUM
  ),
MAT_SPM AS
 (SELECT A.MAT_CMF_1, B.MAT_ID, B.MAT_VER, B.FLOW, B.OPER, B.SPEC_REL_ID
    FROM MAT_LIST A, MESMGR.MSPMRELDEF B
   WHERE A.MAT_ID = B.MAT_ID(+)
     AND A.MAT_VER = B.MAT_VER(+)
     AND A.FLOW = B.FLOW(+)
     AND A.OPER = B.OPER(+)),
SPM_VER AS
 (SELECT C.MAT_CMF_1,
         C.MAT_ID,
         C.MAT_VER,
         C.FLOW,
         C.OPER,
         C.SPEC_REL_ID,
         MAX(D.SPEC_REL_VER) AS SPEC_REL_VER
    FROM MAT_SPM C,
         (SELECT *
            FROM MESMGR.MSPMRELVER
           WHERE APPROVAL_FLAG = 'Y'
             AND RELEASE_FLAG = 'Y') D
   WHERE 1 = 1
     AND C.SPEC_REL_ID = D.SPEC_REL_ID(+)
   GROUP BY C.MAT_CMF_1, C.MAT_ID, C.MAT_VER, C.FLOW, C.OPER, C.SPEC_REL_ID),
CHAR_LIST AS
 (SELECT E.MAT_CMF_1,
         E.MAT_ID,
         E.MAT_VER,
         E.FLOW,
         E.OPER,
         E.SPEC_REL_ID,
         E.SPEC_REL_VER,
         F.CHAR_ID,
         F.LOWER_SPEC_LIMIT,
         F.TARGET_VALUE,
         F.UPPER_SPEC_LIMIT
    FROM SPM_VER E
    LEFT JOIN MESMGR.MSPMRELCHR F
      ON E.SPEC_REL_ID = F.SPEC_REL_ID
     AND E.SPEC_REL_VER = F.SPEC_REL_VER),
CHAR_ATTR AS
 (SELECT *
    FROM (SELECT A.*,
                 B.ATTR_NAME,
                 DECODE(ATTR_VALUE, '[Null]', ' ', ATTR_VALUE) AS ATTR_VALUE
            FROM CHAR_LIST A,
                 (SELECT *
                    FROM MESMGR.MSPMATRSTS
                   WHERE ATTR_NAME IN ('QA_AUDIT_FLAG', 'IE2_AUDIT_FLAG')) B
           WHERE 1 = 1
             AND A.SPEC_REL_ID = B.SPEC_REL_ID(+)
             AND A.SPEC_REL_VER = B.SPEC_REL_VER(+)
             AND A.CHAR_ID = B.CHAR_ID(+))
  PIVOT(MAX(ATTR_VALUE)
     FOR ATTR_NAME IN('QA_AUDIT_FLAG' "QA_AUDIT_FLAG",
                     'IE2_AUDIT_FLAG' "IE2_AUDIT_FLAG"))
   ORDER BY MAT_ID, MAT_VER, FLOW, OPER)
SELECT * FROM CHAR_ATTR WHERE 1 = 1
    """)