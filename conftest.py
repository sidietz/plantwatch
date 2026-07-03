import os
import shutil
import pytest
from django.conf import settings
from django.db import connections

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        for alias in connections:
            if alias == 'plantwatch':
                connection = connections[alias]
                connection.close()
                test_db_path = connection.settings_dict['NAME']
                orig_db_path = os.path.join(settings.BASE_DIR, 'plantwatch.db')
                if os.path.exists(orig_db_path) and orig_db_path != test_db_path:
                    shutil.copyfile(orig_db_path, test_db_path)
