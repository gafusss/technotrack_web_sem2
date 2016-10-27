from django.contrib import admin

# Register your models here.
from m_chat.models import Conference, Dialogue, Message, MessageInclude, ConferenceMembership

admin.site.register(Conference)
admin.site.register(Dialogue)
admin.site.register(ConferenceMembership)
admin.site.register(Message)
admin.site.register(MessageInclude)