from celery import Celery, Task
from . import celery_config


class ZingProductCelery(Celery):
    def gen_task_name(self, name, module):
        module_name_segment_list = module.split('.')
        final_module_name_list = []
        for module_name_segment in module_name_segment_list:
            if module_name_segment == 'tasks':
                continue

            elif module_name_segment == 'data_view_workers':
                module_name_segment = 'data_view'

            final_module_name_list.append(module_name_segment)

        final_module_name = '.'.join(final_module_name_list)
        return super().gen_task_name(name, final_module_name)


app = ZingProductCelery('zing_product')
app.config_from_object(celery_config)
app.autodiscover_tasks(['data_view_workers.test', 'data_view_workers.spx', 'data_view_workers.spv'])