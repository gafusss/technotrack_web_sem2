from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime

from m_comment.models import Comment


def comment_post_save(sender, instance, created, **kwargs):
    if created:
        instance.object.comment_count += 1
        instance.object.last_comment = instance
        instance.object.last_commented_at = datetime.now()


post_save.connect(comment_post_save, Comment, dispatch_uid='tt_comment_post_save')