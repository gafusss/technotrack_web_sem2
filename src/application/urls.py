"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers, serializers, permissions, viewsets
from django.contrib.auth.models import User, Group

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

from m_chat.views import DialogueViewSet, MessageViewSet, ConferenceViewSet, ConferenceMembershipViewSet
from m_comment.views import CommentViewSet
from m_event.views import EventViewSet
from m_like.views import LikeViewSet
from m_photo.views import PhotoAlbumViewSet, PhotoViewSet
from m_post.views import PostViewSet, PostIncludeViewSet
from m_profile.views import FriendshipIncomingViewSet, CommunityProfileViewSet, UserProfileViewSet, FriendshipViewSet
from m_profile.views import FriendshipOutgoingViewSet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'groups', GroupViewSet)

router.register(r'conference', ConferenceViewSet, base_name='conference')
router.register(r'dialogue', DialogueViewSet, base_name='dialogue')
router.register(r'conference_membership', ConferenceMembershipViewSet, base_name='conference_membership')
router.register(r'message', MessageViewSet, base_name='message')
#router.register(r'message_include', MessageIncludeViewSet)

router.register(r'comment', CommentViewSet, base_name='comment')
#router.register(r'comment_include', CommentIncludeViewSet, base_name='comment_include')

router.register(r'event', EventViewSet, base_name='event')

router.register(r'like', LikeViewSet, base_name='like')

router.register(r'photo_album', PhotoAlbumViewSet, base_name='photo_album')
router.register(r'photo', PhotoViewSet, base_name='photo')

router.register(r'post', PostViewSet, base_name='post')
router.register(r'post_include', PostIncludeViewSet, base_name='post_include')

router.register(r'user_profile', UserProfileViewSet, base_name='user_profile')
router.register(r'community_profile', CommunityProfileViewSet, base_name='community_profile')
router.register(r'friendship_incoming', FriendshipIncomingViewSet, base_name='friendship_incoming')
router.register(r'friendship_outgoing', FriendshipOutgoingViewSet, base_name='friendship_outgoing')
router.register(r'friendship', FriendshipViewSet, base_name='friendship')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
