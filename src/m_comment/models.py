from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from rest_framework import permissions

from core.models import EditableMixin, DeletableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin
from m_post.mixins import PostIncludableMixin


class CommentableMixin(models.Model):
    tt_is_commentable = True

    comment_count = models.PositiveIntegerField(default=0,
                                                blank=False,
                                                editable=False,
                                                verbose_name=u'Comment count')
    comment = GenericRelation('m_comment.Comment',
                              object_id_field='object_id',
                              content_type_field='content_type')
    last_commented_at = models.DateTimeField(default=None,
                                             blank=True,
                                             null=True,
                                             verbose_name=u'Last commented at')
    last_comment = models.ForeignKey('m_comment.Comment',
                                     db_index=False,
                                     blank=True,
                                     null=True,
                                     editable=False,
                                     verbose_name=u'Last comment',
                                     related_name=u'last_comment+')

    class Meta:
        abstract = True


class Comment(DeletableMixin, CommentableMixin, EditableMixin, LikeableMixin, CreateEventOnCreateMixin, PostIncludableMixin):
    def get_user_for_event(self):
        return self.sender

    def get_profile_for_event(self):
        return self.profile

    def tt_can_profile_include_in_post(self, profile):
        if self.is_deleted:
            return False
        if hasattr(self.object, 'tt_is_post_includable'):
            return self.object.tt_can_profile_include_in_post(profile)
        else:
            # FIXME: ?
            return False

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.profile == profile or self.object.get_object_permissions_for_profile(method, user, profile)
        if method == 'DELETE':
            # FIXME: Allow delete for object owners somehow
            return self.profile == profile or self.object.get_object_permissions_for_profile(method, user, profile)
        return self.profile == profile

    profile = models.ForeignKey('m_profile.Profile',
                                db_index=True,
                                verbose_name=u'Comment from',
                                related_name='comment',
                                blank=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name=u'Commenter',
                               related_name='comment',
                               on_delete=models.CASCADE,
                               blank=False)
    text = models.TextField(blank=True,
                            verbose_name=u'Comment text')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')

# TODO: DRF this!
class CommentInclude(models.Model):

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.comment.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.comment.get_object_permissions_for_profile(method, user, profile)
        return False

    comment = models.ForeignKey(Comment,
                                db_index=True,
                                verbose_name=u'Comment',
                                related_name='comment_include',
                                blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')
