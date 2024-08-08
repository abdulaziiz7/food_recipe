from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from apps.notification.api.v0.serializers import NotificationSerializer
from apps.notification.models import Notification


class NotificationListAPIView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super(NotificationListAPIView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class NotificationRetrieveAPIView(RetrieveAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = super(NotificationRetrieveAPIView, self).get_object()
        if not obj.read:
            obj.read = True
            obj.save()
        return obj


notification_list = NotificationListAPIView.as_view()
notification_retrieve = NotificationRetrieveAPIView.as_view()
