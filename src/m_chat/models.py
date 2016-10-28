# coding=utf-8

from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: message read?
#  Create your models here.
from core.models import DeletableMixin


class Chat(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      editable=False,
                                      verbose_name=u'Created at')
    last_message = models.ForeignKey('Message',
                                     db_index=False,
                                     blank=True,
                                     null=True,
                                     editable=False,
                                     verbose_name=u'Last message',
                                     related_name=u'last_message+')


class Conference(Chat):
    owner = models.ForeignKey('m_profile.Profile',
                              verbose_name=u'Conference owner',
                              related_name='owned_conference',
                              blank=False)
    members = models.ManyToManyField('m_profile.Profile',
                                     verbose_name=u'Conference members',
                                     related_name='conference',
                                     through='ConferenceMembership',
                                     through_fields=('conference', 'profile'))
    # denorm: is_active == (no inactive memberships)
    is_active = models.BooleanField(blank=False,
                                    default=True,
                                    verbose_name=u'Is active')
    member_count = models.PositiveIntegerField(default=0,
                                               blank=False,
                                               null=False,
                                               verbose_name=u'Member count')

    class Meta:
        index_together = [['owner', 'is_active'], ]


class Dialogue(Chat):
    profile1 = models.ForeignKey('m_profile.Profile',
                                 db_index=True,
                                 verbose_name=u'First person',
                                 related_name='dialogue1',
                                 blank=False)
    profile2 = models.ForeignKey('m_profile.Profile',
                                 db_index=True,
                                 verbose_name=u'Second person',
                                 related_name='dialogue2',
                                 blank=False)


class ConferenceMembership(DeletableMixin):
    conference = models.ForeignKey(Conference,
                                   verbose_name=u'Conference',
                                   related_name='membership',
                                   blank=False)
    profile = models.ForeignKey('m_profile.Profile',
                                verbose_name=u'Invited profile',
                                related_name='conference_membership',
                                blank=False)
    invite_from = models.ForeignKey('m_profile.Profile',
                                    related_name='conference_membership_invite',
                                    verbose_name=u'Invite from',
                                    blank=False)


class Message(DeletableMixin):
    chat = models.ForeignKey(Chat,
                             verbose_name=u'Chat',
                             related_name='message',
                             blank=False)
    sender = models.ForeignKey('m_profile.Profile',
                               verbose_name=u'Sender',
                               related_name='message',
                               blank=False)
    sender_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    verbose_name=u'Sender user',
                                    related_name='message',
                                    blank=False)
    text = models.TextField(blank=True,
                            verbose_name=u'Message text')

    class Meta:
        index_together = [['chat', 'created_at'], ]


class MessageInclude(models.Model):
    message = models.ForeignKey(Message,
                                db_index=True,
                                verbose_name=u'Message',
                                related_name='include',
                                blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')
