from __future__ import unicode_literals

from django.db import models

# Create your models here.

# TODO: FIXME: Decide what the fuck to do with these deletes
from django.utils.datetime_safe import datetime


class DeletableMixin(models.Model):
    is_deleted = models.BooleanField(blank=False,
                                     null=False,
                                     default=False,
                                     verbose_name=u'Is deleted')
    deleted_at = models.DateTimeField(default=None,
                                      blank=True,
                                      null=True,
                                      editable=False,
                                      verbose_name=u'Deleted at')
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=False,
                                      null=False,
                                      editable=False,
                                      verbose_name=u'Created at')

    class Meta:
        abstract = True


class EditableMixin(models.Model):
    last_edited_at = models.DateTimeField(auto_now=True,
                                          verbose_name=u'Last edited at')

    class Meta:
        abstract = True
