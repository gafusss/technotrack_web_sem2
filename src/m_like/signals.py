from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime

from m_like.models import Like


def like_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.dislike:
            instance.object.dislike_count += 1
            instance.object.rating -= 1
        else:
            instance.object.like_count += 1
            instance.object.rating += 1
        instance.object.save()
    else:
        if instance.is_deleted and not instance.is_deleted_was:
            if instance.dislike:
                instance.object.dislike_count -= 1
                instance.object.rating += 1
            else:
                instance.object.like_count -= 1
                instance.object.rating -= 1
            instance.object.save()


post_save.connect(like_post_save, Like, dispatch_uid='tt_like_post_save')
