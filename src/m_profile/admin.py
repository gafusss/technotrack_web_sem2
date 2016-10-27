from django.contrib import admin

# Register your models here.
from m_profile.models import UserProfile, CommunityProfile, Friendship

admin.site.register(UserProfile)
admin.site.register(CommunityProfile)
admin.site.register(Friendship)
