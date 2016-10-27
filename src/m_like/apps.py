from __future__ import unicode_literals

from django.apps import AppConfig


class MLikeConfig(AppConfig):
    name = 'm_like'

    def ready(self):
        import signals