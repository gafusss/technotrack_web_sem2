from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from core.models import EditableMixin, DeletableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin


class CommentableMixin(models.Model):
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


class Comment(DeletableMixin, CommentableMixin, EditableMixin, LikeableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.sender

    def get_profile_for_event(self):
        return self.profile

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


class CommentInclude(models.Model):
    comment = models.ForeignKey(Comment,
                                db_index=True,
                                verbose_name=u'Comment',
                                related_name='comment_include',
                                blank=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey(ct_field='content_type',
                               fk_field='object_id')
