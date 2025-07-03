# from django.apps import AppConfig


# class HrConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'hr'

from django.apps import AppConfig
from django.core.management import call_command
import threading
import time

class HrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hr'

    def ready(self):
        def run_auto_advance():
            while True:
                call_command('auto_advance_leaves')
                time.sleep(600)  # ۱۰ دقیقه

        thread = threading.Thread(target=run_auto_advance, daemon=True)
        thread.start()
