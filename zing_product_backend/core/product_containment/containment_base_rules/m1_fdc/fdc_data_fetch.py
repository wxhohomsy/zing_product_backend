import numpy as np
from zing_product_backend.core.product_containment.containment_constants import IngotFdcField
from .local_db_utils import get_saved_fdc_data_dict, get_saved_diameter_data


def get_ingot_fdc_data(ingot_id: str, target_field: IngotFdcField):
    # diameter is not considered as fdc_data in local_db_utils, which is not consistent with this function
    if target_field is IngotFdcField.DELTA_PS2H50MM_TO_TARGET:
        fdc_data_dict = get_saved_fdc_data_dict(ingot_id)
        format_2h_ps = fdc_data_dict['format_2h_ps']
        format_2h_ps_shift_50 = np.roll(format_2h_ps[50:], 50)
        format_target_ps = fdc_data_dict['format_target_ps']
        return abs(format_2h_ps_shift_50 - format_target_ps)

    elif target_field is IngotFdcField.PS_2H_SHIFT_50MM:
        fdc_data_dict = get_saved_fdc_data_dict(ingot_id)
        format_2h_ps = fdc_data_dict['format_2h_ps']
        return np.roll(format_2h_ps[50:], 50)

    elif target_field is IngotFdcField.DELTA_PS2H50MM_TO_MOVING_AVG:
        fdc_data_dict = get_saved_fdc_data_dict(ingot_id)
        format_2h_ps = fdc_data_dict['format_2h_ps']
        format_2h_ps_shift_50 = np.roll(format_2h_ps[50:], 50)
        format_2h_ps_shift_50_avg = np.convolve(format_2h_ps_shift_50, np.ones(50) / 50, mode='valid')
        return abs(format_2h_ps_shift_50 - format_2h_ps_shift_50_avg)

    elif target_field is IngotFdcField.DIAMETER:
        return get_saved_diameter_data(ingot_id)


