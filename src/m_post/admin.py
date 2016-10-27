from django.contrib import admin

# Register your models here.
from m_post.models import Post, PostInclude

admin.site.register(Post)
admin.site.register(PostInclude)
