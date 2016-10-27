from __future__ import unicode_literals

from django.db import models

from core.models import DeletableMixin, EditableMixin
from m_comment.models import CommentableMixin
from m_event.models import CreateEventOnCreateMixin
from m_like.models import LikeableMixin
from m_profile.models import Profile


# Create your models here.

# TODO: __unicode__ or __str__ (unicode on python2) AND meta verbose_name (_plural) AND unique?
# TODO: on_delete?
# TODO: other fields?

class PhotoAlbum(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.owner

    owner = models.ForeignKey(Profile,
                              db_index=True,
                              verbose_name=u'Album owner',
                              related_name='album',
                              blank=False)
    name = models.CharField(blank=False,
                            max_length=256,
                            verbose_name=u'Album name')
    description = models.TextField(blank=True,
                                   verbose_name=u'Description')


class Photo(DeletableMixin, EditableMixin, LikeableMixin, CommentableMixin, CreateEventOnCreateMixin):
    def get_user_for_event(self):
        return self.album.owner

    album = models.ForeignKey(PhotoAlbum,
                              db_index=True,
                              verbose_name=u'Album',
                              related_name='photo',
                              blank=False)

    # TODO: upload location and filename?
    image = models.ImageField(blank=False,
                              verbose_name=u'Image file',
                              width_field='width',
                              height_field='height')
    height = models.PositiveIntegerField(verbose_name=u'Image height')
    width = models.PositiveIntegerField(verbose_name=u'Image width')

    description = models.TextField(blank=True,
                                   verbose_name=u'Description')