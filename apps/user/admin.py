from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.user.models import User, Follow


@admin.register(User)
class RecipeAdmin(ImportExportModelAdmin):
    fields = ['username', 'first_name', 'last_name', 'phone', 'location']
    list_display = ['pk', 'username']
    search_fields = ['email']


admin.site.register(Follow)
