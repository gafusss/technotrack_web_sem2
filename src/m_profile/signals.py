from django.db.models.signals import pre_save, post_init, post_save
from django.utils import timezone
from django.utils.datetime_safe import datetime

from m_profile.models import Friendship, CommunityProfile


def friendship_post_init(sender, instance, **kwargs):
    instance.is_accepted_was = instance.is_accepted


def friendship_pre_save(sender, instance, **kwargs):
    instance.is_active = instance.is_accepted and not instance.is_deleted
    if instance.is_accepted and not instance.is_accepted_was:
        instance.accepted_at = timezone.now()


def community_profile_post_save(sender, instance, **kwargs):
    for f in instance.friendship_request.filter(is_deleted=False):
        f.is_deleted = True
        f.save()
    for f in instance.friendship_request_sent.filter(is_deleted=False):
        f.is_deleted = True
        f.save()
    #for p in instance.posted.filter(is_deleted=False):
    #    p.is_deleted = True
    #    p.save()
    for p in instance.post.filter(is_deleted=False):
        p.is_deleted = True
        p.save()
    # TODO: Delete all friendships, posts, albums and everything
    pass


pre_save.connect(friendship_pre_save, Friendship, dispatch_uid='tt_friendship_pre_save')
post_init.connect(friendship_post_init, Friendship, dispatch_uid='tt_friendship_post_init')
post_save.connect(community_profile_post_save, CommunityProfile, dispatch_uid='tt_community_profile_post_save')
