from cachetools import cached, TTLCache
import numpy as np
from scipy.interpolate import interpolate, interp1d
from zing_product_backend.app_db.connections import shaiapp02_client
from zing_product_backend import settings
from zing_product_backend.reporting.system_log import server_logger

production_db = shaiapp02_client.m1_data_stats_db
whole_ingot_data_collection = production_db.whole_ingot_data_collection

FDC_CACHE_SIZE = 50
FDC_CACHE_TIME = 1800


@cached(cache=TTLCache(maxsize=FDC_CACHE_SIZE, ttl=FDC_CACHE_TIME), info=settings.DEBUG)
def get_saved_fdc_data_dict(ingot_id: str):
    saved_data_dict = whole_ingot_data_collection.find_one({'ingot_id': ingot_id},
                                                           {'fdc_data.pull_speed_2h_avg': 1,
                                                            'fdc_data.length': 1,
                                                            'fdc_data.target_pull_speed': 1,
                                                            })
    if saved_data_dict is None or 'fdc_data' not in saved_data_dict:
        server_logger.error(f'ingot_id: {ingot_id} does not have saved fdc data')

    length_list = saved_data_dict['fdc_data']['length']
    raw_pull_spead_2h_list = saved_data_dict['fdc_data']['pull_speed_2h_avg']
    raw_target_pull_speed_list = saved_data_dict['fdc_data']['target_pull_speed']
    interpolate_function_2h_speed = interp1d(length_list, raw_pull_spead_2h_list, kind='linear',
                                             assume_sorted=True)
    interpolate_function_target_speed = interp1d(length_list, raw_target_pull_speed_list, kind='linear',
                                                 assume_sorted=True)

    format_2h_ps = np.arange(int(length_list[0]), int(length_list[-1] + 1))
    format_2h_ps = interpolate_function_2h_speed(format_2h_ps)
    format_target_ps = interpolate_function_target_speed(format_2h_ps)
    return {
        'format_2h_ps': format_2h_ps,
        'format_target_ps': format_target_ps
    }


@cached(cache=TTLCache(maxsize=FDC_CACHE_SIZE, ttl=FDC_CACHE_TIME), info=settings.DEBUG)
def get_saved_diameter_data(ingot_id: str) -> np.array:
    saved_data_dict = whole_ingot_data_collection.find_one({'ingot_id': ingot_id},
                                                           {'dia_data.length': 1,
                                                            'dia_data.diameter': 1,
                                                            })
    if saved_data_dict is None or 'dia_data' not in saved_data_dict:
        server_logger.error(f'ingot_id: {ingot_id} does not have saved diameter data')

    length_list = saved_data_dict['dia_data']['length']
    diameter_list = saved_data_dict['dia_data']['diameter']
    interpolate_function_diameter = interp1d(length_list, diameter_list, kind='linear',
                                             assume_sorted=True)
    format_length = np.arange(int(length_list[0]), int(length_list[-1] + 1))
    format_diameter = interpolate_function_diameter(format_length)
    return format_diameter
