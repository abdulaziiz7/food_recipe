from django.urls import path

from apps.notification.api.v0.views import notification_list, notification_retrieve

urlpatterns = [
    path('notification-list/', notification_list, name='notification_list'),
    path('notification-retrieve/<int:pk>', notification_retrieve, name='notification_retrieve')
]
