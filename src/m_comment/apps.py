from __future__ import unicode_literals

from django.apps import AppConfig


class MCommentConfig(AppConfig):
    name = 'm_comment'

    def ready(self):
        import signals