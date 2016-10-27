from django.db.models.signals import post_save, post_init
from django.utils.datetime_safe import datetime

from core.models import DeletableMixin
from m_comment.models import Comment


def deletable_mixin_post_init(sender, instance):
    instance.is_deleted_was = instance.is_deleted

for e in DeletableMixin.__subclasses__():
    post_init.connect(deletable_mixin_post_init, e)
