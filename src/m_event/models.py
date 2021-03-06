from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
# TODO: FIXME: Deletable? On delete? wtf
from rest_framework import permissions


class Event(models.Model):

    def get_object_permissions_for_profile(self, method, user, profile):
        if profile is None:
            return False
        if method in permissions.SAFE_METHODS:
            if self.profile == profile or self.profile.is_friends_with_profile(profile):
                return True
        return False

    profile = models.ForeignKey('m_profile.Profile',
                                db_index=True,
                                verbose_name=u'Origin',
                                related_name='event',
                                blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=u'By user',
                             related_name='event',
                             blank=False)
    timestamp = models.DateTimeField(auto_now_add=True,
                                     blank=False,
                                     null=False,
                                     verbose_name=u'Timestamp')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')


class CreateEventOnCreateMixin(models.Model):
    def get_user_for_event(self):
        raise Exception('FuckThatImNotDoingThatShitERROR')

    def get_profile_for_event(self):
        raise Exception('FuckThatImNotDoingThatShitERROR')

    class Meta:
        abstract = True
