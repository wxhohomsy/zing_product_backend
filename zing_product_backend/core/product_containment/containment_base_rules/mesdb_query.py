import typing
from zing_product_backend.app_db.mes_db_query import get_cdb_engine, get_lot_sts,  get_sublot_sts
if typing.TYPE_CHECKING:
    from zing_product_backend.core.product_containment.parser_core.containment_structure import Product, LotLikeProduct, SublotProduct


def get_material_from_product(target_product: 'Product') -> str:
    target_product_v_factory = target_product.virtual_factory
    if isinstance(target_product, LotLikeProduct):
        lot_sts = get_lot_sts(target_product_v_factory, target_product.id)
        mat_id = lot_sts['mat_id']
    elif isinstance(target_product, SublotProduct):
        sublot_sts = get_sublot_sts(target_product_v_factory, target_product.id)
        mat_id = sublot_sts['mat_id']

    else:
        raise ValueError(f'Unknown product type: {target_product}')

    return mat_id

