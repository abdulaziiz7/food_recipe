from django.contrib import admin

from apps.user.models import User, Follow, PasswordReset

admin.site.register(User)
admin.site.register(Follow)
admin.site.register(PasswordReset)
