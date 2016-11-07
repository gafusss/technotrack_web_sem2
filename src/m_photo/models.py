from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from rest_framework import permissions

from core.models import DeletableMixin, EditableMixin
from m_comment.models import CommentableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin
from m_post.mixins import PostIncludableMixin
from m_profile.models import Profile


# Create your models here.

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: other fields?

class PhotoAlbum(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin, PostIncludableMixin):
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
            if self.profile == profile or self.profile.is_friends_with(profile):
                return True
            else:
                return False
        if self.profile == profile:
            return True
        else:
            return False

    profile = models.ForeignKey(Profile,
                                db_index=True,
                                verbose_name=u'Album owner',
                                related_name='album',
                                blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'By user',
                             related_name='album',
                             blank=False)
    name = models.CharField(blank=False,
                            max_length=256,
                            verbose_name=u'Album name')
    description = models.TextField(blank=True,
                                   verbose_name=u'Description')


class Photo(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin, PostIncludableMixin):
    def get_user_for_event(self):
        return self.user

    def get_profile_for_event(self):
        return self.profile

    def tt_can_profile_include_in_post(self, profile):
        return self.get_object_permissions_for_profile('GET', None, profile)

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        return self.album.get_object_permissions_for_profile(method, user, profile)

    album = models.ForeignKey(PhotoAlbum,
                              db_index=True,
                              verbose_name=u'Album',
                              related_name='photo',
                              blank=False)
    profile = models.ForeignKey(Profile,
                                db_index=True,
                                verbose_name=u'Added by',
                                related_name='photo',
                                blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'By user',
                             related_name='photo',
                             blank=False)

    # TODO: upload location and filename?
    image = models.ImageField(blank=False,
                              verbose_name=u'Image file',
                              width_field='width',
                              height_field='height')
    height = models.PositiveIntegerField(verbose_name=u'Image height')
    width = models.PositiveIntegerField(verbose_name=u'Image width')

    description = models.TextField(blank=True,
                                   verbose_name=u'Description')
