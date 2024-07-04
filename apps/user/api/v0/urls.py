from django.urls import path

from apps.user.api.v0.views import user_create, user_update, following_create, user_login, followers_list, \
    following_list, user_profile

app_name = 'user_api'

urlpatterns = [
    path('create/', user_create, name='create'),
    path('update/<int:pk>', user_update, name='update'),
    path('login/', user_login, name='login'),
    path('profile/', user_profile, name='profile'),
    path('following/', following_create, name='following_create'),
    path('followers_list/', followers_list, name='followers'),
    path('following_list/', following_list, name='followings')
]
