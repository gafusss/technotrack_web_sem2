from __future__ import unicode_literals

from django.apps import AppConfig


class MPostConfig(AppConfig):
    name = 'm_post'
    def ready(self):
        import signals