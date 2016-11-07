from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from rest_framework import permissions

from core.models import DeletableMixin, EditableMixin

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: other fields? descr fields, time fields!
# TODO: db_index=True and meta: index_together [["f1", "f2"],]
# Create your models here.
from m_comment.models import CommentableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin
from m_post.mixins import PostIncludableMixin


class Post(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin,
           PostIncludableMixin):
    def get_user_for_event(self):
        return self.user

    def get_profile_for_event(self):
        return self.profile

    def tt_can_profile_include_in_post(self, profile):
        return self.get_object_permissions_for_profile('GET', None, profile)

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            if self.profile == profile \
                    or self.sender == profile \
                    or (self.sender == self.profile or self.profile.is_friends_with(profile)):
                return True
            else:
                return False
        if method == 'DELETE':
            if self.sender == profile or self.profile == profile:
                return True
            else:
                return False
        # POST, PUT, PATCH
        if self.sender == profile:
            return True
        return False

    profile = models.ForeignKey('m_profile.Profile',
                                db_index=True,
                                verbose_name=u'Posted to',
                                related_name='post',
                                blank=False)
    sender = models.ForeignKey('m_profile.Profile',
                               verbose_name=u'Sender',
                               related_name='posted',
                               blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'By user',
                             related_name='post',
                             blank=False)
    text = models.TextField(blank=True,
                            verbose_name=u'Post text')
    repost_count = models.PositiveIntegerField(default=0,
                                               blank=False,
                                               editable=False,
                                               verbose_name=u'Repost count')


# TODO: FIXME: Link class;

class PostInclude(models.Model):

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.message.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.message.profile == profile or self.message.get_object_permissions_for_profile(method, user, profile)
        return False

    message = models.ForeignKey(Post,
                                db_index=True,
                                verbose_name=u'Post',
                                related_name='post_include',
                                blank=False,
                                on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')

    class Meta:
        unique_together = ('message', 'content_type', 'object_id')
