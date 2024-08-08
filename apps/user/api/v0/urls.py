from django.urls import path

from apps.user.api.v0.views import user_create, user_update, following_create, user_login, followers_list, \
    following_list, user_profile, verify_code, change_password, reset_password, forgot_password

app_name = 'user_api'

urlpatterns = [
    path('create/', user_create, name='create'),
    path('update/<int:pk>', user_update, name='update'),
    path('login/', user_login, name='login'),
    path('verify-code/', verify_code, name='verify'),
    path('profile/', user_profile, name='profile'),
    path('change-password/', change_password, name='change_password'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:token>', reset_password, name='reset_password'),
    path('following/', following_create, name='following_create'),
    path('followers_list/', followers_list, name='followers'),
    path('following_list/', following_list, name='followings')
]
