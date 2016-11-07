from django.db import models


class PostIncludableMixin(models.Model):
    tt_is_post_includable = True

    def tt_can_profile_include_in_post(self, profile):
        return False

    class Meta:
        abstract = True
