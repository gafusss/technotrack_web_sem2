from __future__ import unicode_literals

from django.apps import AppConfig


class MChatConfig(AppConfig):
    name = 'm_chat'

    def ready(self):
        import signals
