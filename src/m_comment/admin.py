from django.contrib import admin

# Register your models here.
from m_comment.models import Comment, CommentInclude

admin.site.register(Comment)
admin.site.register(CommentInclude)
