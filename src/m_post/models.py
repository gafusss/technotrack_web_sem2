from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models

from core.models import DeletableMixin, EditableMixin


# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: other fields? descr fields, time fields!
# TODO: db_index=True and meta: index_together [["f1", "f2"],]
# Create your models here.
from m_comment.models import CommentableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin


class Post(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.user

    def get_profile_for_event(self):
        return self.sender

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
    message = models.ForeignKey(Post,
                                db_index=True,
                                verbose_name=u'Post',
                                related_name='post_include',
                                blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')
