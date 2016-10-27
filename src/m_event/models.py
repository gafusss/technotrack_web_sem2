from __future__ import unicode_literals

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
# TODO: SIGNALS FOR GENERATING EVENTS

# TODO: FIXME: Deletable? On delete? wtf
class Event(models.Model):
    profile = models.ForeignKey('m_profile.Profile',
                                db_index=True,
                                verbose_name=u'Origin',
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
        pass

    class Meta:
        abstract = True
