from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from m_post.models import Post


def post_post_save(sender, instance, created, **kwargs):
    if created:
        for e in instance.post_include_set.filter(content_type=ContentType.objects.get_for_model(Post)):
            e.repost_count += 1
            e.save()
    else:
        if instance.is_deleted and not instance.is_deleted_was:
            for e in instance.post_include_set.filter(content_type=ContentType.objects.get_for_model(Post)):
                e.repost_count -= 1
                e.save()

post_save.connect(post_post_save, Post, dispatch_uid='tt_post_post_save')
