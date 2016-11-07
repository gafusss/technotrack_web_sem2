from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from rest_framework import permissions

from core.models import DeletableMixin
from m_event.models import CreateEventOnCreateMixin


class Like(DeletableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.user

    def get_profile_for_event(self):
        return self.profile

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None or self.is_deleted:
            return False
        if method in permissions.SAFE_METHODS:
            return self.profile == profile or self.object.get_object_permissions_for_profile(method, user, profile)
        if method == 'DELETE':
            return self.profile == profile
        # Don't allow to change likes. Delete old and create new, pls
        return False

    profile = models.ForeignKey('m_profile.Profile',
                                verbose_name=u'Like from',
                                related_name='like',
                                blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'By user',
                             related_name='like',
                             blank=False)
    dislike = models.BooleanField(blank=False,
                                  null=False,
                                  default=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')

    class Meta:
        index_together = [['profile', 'dislike'], ]


class LikeableMixin(models.Model):

    tt_is_likeable = True

    def get_like_for_profile(self, profile):
        l = profile.like.filter(is_deleted=False).filter(object_id=self.id, content_type=ContentType.objects.get_for_model(self))
        return l.first()

    like_count = models.PositiveIntegerField(default=0,
                                             blank=False,
                                             editable=False,
                                             verbose_name=u'Like count')
    dislike_count = models.PositiveIntegerField(default=0,
                                                blank=False,
                                                editable=False,
                                                verbose_name=u'Dislike count')
    rating = models.IntegerField(default=0,
                                 blank=False,
                                 editable=False,
                                 verbose_name=u'Rating')
    like = GenericRelation(Like,
                           object_id_field='object_id',
                           content_type_field='content_type')

    class Meta:
        abstract = True
