from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from m_post.models import Post, PostInclude


def post_include_post_save(sender, instance, created, **kwargs):
    if created:
        if instance.content_type == ContentType.objects.get_for_model(Post):
            instance.object.repost_count += 1
            instance.object.save()
    else:
        if instance.is_deleted and not instance.is_deleted_was:
            if instance.content_type == ContentType.objects.get_for_model(Post):
                instance.object.repost_count -= 1
                instance.object.save()


post_save.connect(post_include_post_save, PostInclude, dispatch_uid='tt_post_include_post_save')
