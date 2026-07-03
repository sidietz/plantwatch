import os
import shutil
from django.test.runner import DiscoverRunner

class PlantwatchTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        old_config = super().setup_databases(**kwargs)
        for connection, old_name, destroy in old_config:
            if connection.alias == 'plantwatch':
                connection.close()
                test_db_path = connection.settings_dict['NAME']
                if old_name and os.path.exists(old_name) and old_name != test_db_path:
                    shutil.copyfile(old_name, test_db_path)
        return old_config
