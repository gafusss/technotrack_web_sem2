from django.db.models.signals import post_save, post_init, pre_save
from django.utils import timezone
from django.utils.datetime_safe import datetime

from core.models import DeletableMixin
from m_comment.models import Comment


def deletable_mixin_post_init(sender, instance, **kwargs):
    instance.is_deleted_was = instance.is_deleted


def deletable_mixin_pre_save(sender, instance, **kwargs):
    if instance.is_deleted and not instance.is_deleted_was:
        instance.deleted_at = timezone.now()

for e in DeletableMixin.__subclasses__():
    post_init.connect(deletable_mixin_post_init, e, dispatch_uid='tt_deletable_mixin'+repr(e)+'_post_init')
    pre_save.connect(deletable_mixin_pre_save, e, dispatch_uid='tt_deletable_mixin_'+repr(e)+'_pre_save')
