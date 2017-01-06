#!/usr/bin/env python
import os
import sys

import dotenv


if __name__ == "__main__":

    dotenv.read_dotenv()

    os.environ.setdefault('DB_ENGINE', 'django.contrib.gis.db.backends.postgis')
    os.environ.setdefault('DB_NAME', 'WastyDB')
    os.environ.setdefault('DB_USER', 'postgres')
    os.environ.setdefault('DB_PASSWORD', 'postgres')
    os.environ.setdefault('DB_HOST', '141.115.103.5')
    os.environ.setdefault('DB_PORT', '8000')
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('SECRET_KEY', 'a_default_secret_key_is_not_safe')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wastydb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
