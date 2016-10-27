from django.db.models.signals import post_save

from m_chat.models import Message, ConferenceMembership


def message_post_save(sender, instance, created, **kwargs):
    if created:
        instance.chat.last_message = instance
        instance.chat.save()


def conference_membership_post_save(sender, instance, created, **kwargs):
    if created:
        instance.conference.member_count += 1
        instance.conference.is_active = True
        instance.conference.save()
    else:
        if instance.is_deleted:
            instance.conference.member_count -= 1


post_save.connect(message_post_save, Message, dispatch_uid='tt_message_post_save')
post_save.connect(conference_membership_post_save,
                  ConferenceMembership,
                  dispatch_uid='tt_conference_membership_post_save')