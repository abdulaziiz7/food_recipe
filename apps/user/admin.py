from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.user.models import User, Follow, PasswordReset


@admin.register(User)
class RecipeAdmin(ImportExportModelAdmin):
    fields = [
        'username', 'first_name',
        'last_name', 'phone',
        'birthday', 'location',
        'about_me'
    ]
    list_display = ['pk', 'username']
    search_fields = ['email']


admin.site.register(Follow)
admin.site.register(PasswordReset)
