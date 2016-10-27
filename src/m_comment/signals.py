from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime

from m_comment.models import Comment


def comment_post_save(sender, instance, created, **kwargs):
    if created:
        instance.object.comment_count += 1
        instance.object.last_comment = instance
        instance.object.last_commented_at = instance.created_at
        instance.object.save()
    else:
        if instance.is_deleted and not instance.is_deleted_was:
            instance.object.comment_count -= 1
            instance.object.last_comment = Comment.objects\
                .filter(object=instance.object)\
                .filter(is_deleted=False)\
                .order_by('-created_at')\
                .first()
            instance.object.last_commented_at = instance.object.last_comment.created_at or None
            instance.object.save()


post_save.connect(comment_post_save, Comment, dispatch_uid='tt_comment_post_save')