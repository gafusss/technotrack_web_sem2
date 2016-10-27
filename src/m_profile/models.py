# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from core.models import DeletableMixin, EditableMixin
from m_like.models import LikeableMixin


# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: other fields in profiles
# Create your models here.


class Profile(EditableMixin, LikeableMixin):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=u'Profile owner',
                              related_name='profile',
                              on_delete=models.CASCADE,
                              blank=False)

    # # denorm: active friends
    # friend = models.ManyToManyField('self',
    #                                 verbose_name=u'Friends',
    #                                 related_name='friend',
    #                                 symmetrical=True)
    # # denorm: active chats
    # chat = models.ManyToManyField('m_chat.Chat',
    #                               verbose_name=u'Chats',
    #                               symmetrical=False)
    # TODO: denorm: number of friends, friend requests, other shit, every fucking counter
    # TODO: avatar = foreign key to photos? cut box? wtf?


class UserProfile(Profile):
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    first_name = models.CharField(max_length=100,
                                  blank=False,
                                  verbose_name=u'First name')
    last_name = models.CharField(max_length=100,
                                 blank=False,
                                 verbose_name=u'Last name')
    gender = models.BooleanField(default=True,
                                 blank=False,
                                 null=False,
                                 verbose_name=u'Gender (male?)')
    birthday = models.DateField(blank=False,
                                null=False,
                                verbose_name=u'Birthday')


class CommunityProfile(DeletableMixin, Profile):

    name = models.CharField(blank=False,
                            max_length=256,
                            verbose_name=u'Community name')
    description = models.TextField(blank=True,
                                   verbose_name=u'Description')


class Friendship(DeletableMixin):
    # is magic

    request_from = models.ForeignKey(Profile,
                                     related_name='friendship_request_sent',
                                     verbose_name=u'Request from',
                                     blank=False)
    request_to = models.ForeignKey(Profile,
                                   related_name='friendship_request',
                                   verbose_name=u'Request to',
                                   blank=False)
    # is_active == (accepted and not deleted)
    is_active = models.BooleanField(blank=False,
                                    default=False,
                                    verbose_name=u'Is active')

    # is_accepted == (accepted_at is not blank)
    is_accepted = models.BooleanField(blank=False,
                                      default=False,
                                      verbose_name=u'Is accepted')

    accepted_at = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       verbose_name=u'Accepted at')
    request_text = models.TextField(blank=True,
                                    verbose_name=u'Request text')

    class Meta:
        index_together = [
            ['request_from', 'is_active'],
            ['request_to', 'is_active'],
        ]
