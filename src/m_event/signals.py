from m_event.models import Event


def create_event_on_create_mixin_post_save(sender, instance, created, **kwargs):
    if created:
        e = Event(profile=instance.get_profile_for_event(),
                  user=instance.get_user_for_event(),
                  object=instance)
        e.save()
