from __future__ import unicode_literals

from django.apps import AppConfig


class MProfileConfig(AppConfig):
    name = 'm_profile'

    def ready(self):
        import signals
