from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^(?P<id>\d+)$', views.show_user_page),
    url(r'^process$', views.process, name = 'process'),
    url(r'^adduser$', views.adduser, name = 'adduser'),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^update_profile$', views.update_profile),
    url(r'^profile_pic$', views.profile_pic),
    
    url(r'^(?P<id>\d+)/friends$', views.display_all_friends),
    url(r'^(?P<id>\d+)/friends_process$', views.friends_process),
    url(r'^(?P<id>\d+)/friends_online$', views.friends_online),
    url(r'^(?P<id>\d+)/friends_others$', views.friends_others),
    url(r'^(?P<id>\d+)/friend/delete$', views.friends_delete),
    url(r'^(?P<id>\d+)/friend_online/delete$', views.friends_delete_online),
    
    url(r'^(?P<id>\d+)/messages$', views.display_messages),
    url(r'^(?P<id>\d+)/send_messages$', views.send_messages),
    url(r'^(?P<id>\d+)/new_message$', views.new_message),
    url(r'^check_new_message$', views.check_new_message),

    url(r'^(?P<id>\d+)/groups$', views.display_groups),
    url(r'^(?P<id>\d+)/my_groups$', views.display_my_groups),
    url(r'^(?P<id>\d+)/admin_groups$', views.display_admin_groups),
    url(r'^(?P<id>\d+)/other_groups$', views.display_other_groups),

    url(r'^(?P<id>\d+)/delete_group$', views.delete_group),
    url(r'^(?P<id>\d+)/follow_group/(?P<group_id>\d+)$', views.follow_group),
    url(r'^(?P<id>\d+)/unfollow_group/(?P<group_id>\d+)$', views.unfollow_group),
    url(r'^(?P<id>\d+)/follow/group/(?P<group_id>\d+)$', views.followGroup),
    url(r'^(?P<id>\d+)/unfollow/group/(?P<group_id>\d+)$', views.unfollowGroup),

    url(r'^(?P<id>\d+)/display_group/(?P<id_group>\d+)$', views.display_group),
    url(r'^(?P<id>\d+)/create_group$', views.create_group),
    url(r'^(?P<id>\d+)/display_group/update_title$', views.update_title),
    url(r'^(?P<id>\d+)/display_group/update_desc$', views.update_desc),
    url(r'^(?P<id>\d+)/display_group/group_pic$', views.group_pic),
    
    url(r'^add_to_friend/(?P<id>\d+)$', views.add_to_friend),
    url(r'^(?P<id>\d+)/post_process$', views.post_process),
    url(r'^(?P<id>\d+)/comment_process$', views.comment_process),
    url(r'^(?P<id>\d+)/post_delete$', views.post_delete),
    url(r'^delete_comment$', views.delete_comment),
    url(r'^(?P<id>\d+)/display_my_posts$', views.display_my_posts),
    url(r'^(?P<id>\d+)/display_all_posts$', views.display_all_posts),
    url(r'^like_post$', views.like_post),
    url(r'^like_comment$', views.like_comment),

    url(r'^my_pic$', views.my_pic),
    url(r'^(?P<id>\d+)/more_pic_upload$', views.more_pic_upload),
    url(r'^(?P<id>\d+)/pics$', views.display_user_pics),
    url(r'^(?P<id>\d+)/delete_pic/(?P<id_pic>\d+)$', views.delete_pic),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)