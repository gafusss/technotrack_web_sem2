from __future__ import unicode_literals

from django.apps import AppConfig


class MEventConfig(AppConfig):
    name = 'm_event'

    def ready(self):
        import signals