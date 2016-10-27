from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from core.models import DeletableMixin
from m_event.models import CreateEventOnCreateMixin


class Like(DeletableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.profile

    profile = models.ForeignKey('m_profile.Profile',
                                verbose_name=u'Like from',
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
